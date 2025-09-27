from fastapi import APIRouter, HTTPException, status, Depends
from typing import List, Optional
from models import (
    DSAProblem, DSASubmission, DSAUserProgress, DSADiscussion,
    DSADifficulty, DSACategory, DSATopic, DSAChapter
)
from database import get_database
from user_auth import get_current_user
from datetime import datetime
import json

dsa_router = APIRouter(prefix="/dsa", tags=["dsa-problems"])

# Get all DSA categories
@dsa_router.get("/categories")
async def get_dsa_categories():
    """Get all DSA categories"""
    try:
        db = await get_database()
        categories = await db.dsa_categories.find({}).to_list(100)
        return {"categories": categories}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch categories: {str(e)}")

# Get topics by category
@dsa_router.get("/categories/{category_id}/topics")
async def get_topics_by_category(category_id: str):
    """Get topics for a specific category"""
    try:
        db = await get_database()
        topics = await db.dsa_topics.find({"category_id": category_id}).to_list(100)
        return {"topics": topics}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch topics: {str(e)}")

# Get problems with filters
@dsa_router.get("/problems")
async def get_dsa_problems(
    topic_id: Optional[str] = None,
    difficulty: Optional[DSADifficulty] = None,
    category_id: Optional[str] = None,
    search: Optional[str] = None,
    limit: int = 20,
    skip: int = 0
):
    """Get DSA problems with optional filters"""
    try:
        db = await get_database()
        
        filter_criteria = {"status": "published"}
        
        if topic_id:
            filter_criteria["topic_id"] = topic_id
        if difficulty:
            filter_criteria["difficulty"] = difficulty
        if category_id:
            filter_criteria["category_id"] = category_id
        if search:
            filter_criteria["$or"] = [
                {"title": {"$regex": search, "$options": "i"}},
                {"tags": {"$in": [search]}}
            ]
        
        problems = await db.dsa_problems.find(filter_criteria).skip(skip).limit(limit).to_list(limit)
        total_count = await db.dsa_problems.count_documents(filter_criteria)
        
        return {
            "problems": problems,
            "total": total_count,
            "page": (skip // limit) + 1,
            "total_pages": (total_count + limit - 1) // limit
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch problems: {str(e)}")

# Get specific problem details
@dsa_router.get("/problems/{problem_id}")
async def get_problem_details(problem_id: str, current_user = Depends(get_current_user)):
    """Get detailed information about a specific DSA problem"""
    try:
        db = await get_database()
        
        problem = await db.dsa_problems.find_one({"id": problem_id})
        if not problem:
            raise HTTPException(status_code=404, detail="Problem not found")
        
        # Get user's progress for this problem
        user_progress = await db.dsa_user_progress.find_one({
            "user_id": current_user.id,
            "problem_id": problem_id
        })
        
        # Get user's submissions
        submissions = await db.dsa_submissions.find({
            "user_id": current_user.id,
            "problem_id": problem_id
        }).sort("submitted_at", -1).limit(10).to_list(10)
        
        # Update view count
        await db.dsa_problems.update_one(
            {"id": problem_id},
            {"$inc": {"attempts": 1}}
        )
        
        return {
            "problem": problem,
            "user_progress": user_progress,
            "recent_submissions": submissions
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch problem details: {str(e)}")

# Submit solution
@dsa_router.post("/problems/{problem_id}/submit")
async def submit_solution(
    problem_id: str,
    submission_data: dict,
    current_user = Depends(get_current_user)
):
    """Submit a solution for a DSA problem"""
    try:
        db = await get_database()
        
        # Verify problem exists
        problem = await db.dsa_problems.find_one({"id": problem_id})
        if not problem:
            raise HTTPException(status_code=404, detail="Problem not found")
        
        # Create submission record
        submission = DSASubmission(
            problem_id=problem_id,
            user_id=current_user.id,
            code=submission_data.get("code", ""),
            language=submission_data.get("language", "python"),
            status="pending"  # Will be updated after test execution
        )
        
        # Simple test case validation (in a real system, this would run in a sandboxed environment)
        test_cases = problem.get("test_cases", [])
        passed_cases = 0
        
        # Mock execution result (replace with actual code execution)
        if submission_data.get("code"):
            # For demo purposes, randomly determine pass/fail
            import random
            passed_cases = random.randint(0, len(test_cases))
            submission.test_cases_passed = passed_cases
            submission.total_test_cases = len(test_cases)
            submission.status = "accepted" if passed_cases == len(test_cases) else "wrong_answer"
        
        # Insert submission
        await db.dsa_submissions.insert_one(submission.dict())
        
        # Update user progress
        user_progress = await db.dsa_user_progress.find_one({
            "user_id": current_user.id,
            "problem_id": problem_id
        })
        
        if user_progress:
            # Update existing progress
            updates = {
                "attempts": user_progress["attempts"] + 1,
                "last_attempted": datetime.utcnow()
            }
            
            if submission.status == "accepted":
                updates["status"] = "solved"
                updates["solved_at"] = datetime.utcnow()
                updates["best_solution"] = submission.code
                updates["best_language"] = submission.language
            
            await db.dsa_user_progress.update_one(
                {"user_id": current_user.id, "problem_id": problem_id},
                {"$set": updates}
            )
        else:
            # Create new progress record
            progress = DSAUserProgress(
                user_id=current_user.id,
                problem_id=problem_id,
                status="solved" if submission.status == "accepted" else "in_progress",
                attempts=1,
                best_solution=submission.code if submission.status == "accepted" else None,
                best_language=submission.language if submission.status == "accepted" else None,
                solved_at=datetime.utcnow() if submission.status == "accepted" else None
            )
            await db.dsa_user_progress.insert_one(progress.dict())
        
        # Update problem statistics
        await db.dsa_problems.update_one(
            {"id": problem_id},
            {
                "$inc": {
                    "attempts": 1,
                    "solved_count": 1 if submission.status == "accepted" else 0
                }
            }
        )
        
        return {
            "submission_id": submission.id,
            "status": submission.status,
            "test_cases_passed": submission.test_cases_passed,
            "total_test_cases": submission.total_test_cases,
            "message": "Solution submitted successfully"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to submit solution: {str(e)}")

# Get problem hints
@dsa_router.get("/problems/{problem_id}/hints")
async def get_problem_hints(problem_id: str, current_user = Depends(get_current_user)):
    """Get hints for a DSA problem"""
    try:
        db = await get_database()
        
        problem = await db.dsa_problems.find_one({"id": problem_id})
        if not problem:
            raise HTTPException(status_code=404, detail="Problem not found")
        
        return {"hints": problem.get("hints", [])}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch hints: {str(e)}")

# Get problem solution
@dsa_router.get("/problems/{problem_id}/solution")
async def get_problem_solution(problem_id: str, current_user = Depends(get_current_user)):
    """Get solution approach for a DSA problem"""
    try:
        db = await get_database()
        
        problem = await db.dsa_problems.find_one({"id": problem_id})
        if not problem:
            raise HTTPException(status_code=404, detail="Problem not found")
        
        # Check if user has attempted the problem
        user_progress = await db.dsa_user_progress.find_one({
            "user_id": current_user.id,
            "problem_id": problem_id
        })
        
        if not user_progress or user_progress["attempts"] == 0:
            raise HTTPException(status_code=403, detail="Attempt the problem first to view solution")
        
        return {
            "solution_approach": problem.get("solution_approach", ""),
            "time_complexity": problem.get("time_complexity", ""),
            "space_complexity": problem.get("space_complexity", ""),
            "user_best_solution": user_progress.get("best_solution", "")
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch solution: {str(e)}")

# Discussion endpoints
@dsa_router.get("/problems/{problem_id}/discussions")
async def get_problem_discussions(problem_id: str, limit: int = 20, skip: int = 0):
    """Get discussions for a DSA problem"""
    try:
        db = await get_database()
        
        discussions = await db.dsa_discussions.find({
            "problem_id": problem_id,
            "parent_id": None  # Only top-level discussions
        }).sort("created_at", -1).skip(skip).limit(limit).to_list(limit)
        
        # Get replies for each discussion
        for discussion in discussions:
            replies = await db.dsa_discussions.find({
                "parent_id": discussion["id"]
            }).sort("created_at", 1).to_list(10)
            discussion["replies"] = replies
        
        return {"discussions": discussions}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch discussions: {str(e)}")

@dsa_router.post("/problems/{problem_id}/discussions")
async def create_discussion(
    problem_id: str,
    discussion_data: dict,
    current_user = Depends(get_current_user)
):
    """Create a new discussion or reply for a DSA problem"""
    try:
        db = await get_database()
        
        discussion = DSADiscussion(
            problem_id=problem_id,
            user_id=current_user.id,
            user_name=current_user.email.split("@")[0],  # Simple username extraction
            content=discussion_data.get("content", ""),
            is_solution=discussion_data.get("is_solution", False),
            parent_id=discussion_data.get("parent_id")
        )
        
        await db.dsa_discussions.insert_one(discussion.dict())
        
        return {"message": "Discussion created successfully", "discussion_id": discussion.id}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create discussion: {str(e)}")

# Get user's DSA progress summary
@dsa_router.get("/progress")
async def get_user_progress(current_user = Depends(get_current_user)):
    """Get user's overall DSA progress"""
    try:
        db = await get_database()
        
        # Get total problems count by difficulty
        total_problems = await db.dsa_problems.aggregate([
            {"$match": {"status": "published"}},
            {"$group": {"_id": "$difficulty", "count": {"$sum": 1}}}
        ]).to_list(10)
        
        # Get user's solved problems by difficulty
        solved_problems = await db.dsa_user_progress.aggregate([
            {"$match": {"user_id": current_user.id, "status": "solved"}},
            {
                "$lookup": {
                    "from": "dsa_problems",
                    "localField": "problem_id",
                    "foreignField": "id",
                    "as": "problem"
                }
            },
            {"$unwind": "$problem"},
            {"$group": {"_id": "$problem.difficulty", "count": {"$sum": 1}}}
        ]).to_list(10)
        
        # Format progress data
        progress_summary = {
            "total_solved": sum(item["count"] for item in solved_problems),
            "total_problems": sum(item["count"] for item in total_problems),
            "by_difficulty": {
                "easy": {"solved": 0, "total": 0},
                "medium": {"solved": 0, "total": 0},
                "hard": {"solved": 0, "total": 0}
            }
        }
        
        # Populate totals
        for item in total_problems:
            if item["_id"] in progress_summary["by_difficulty"]:
                progress_summary["by_difficulty"][item["_id"]]["total"] = item["count"]
        
        # Populate solved counts
        for item in solved_problems:
            if item["_id"] in progress_summary["by_difficulty"]:
                progress_summary["by_difficulty"][item["_id"]]["solved"] = item["count"]
        
        return progress_summary
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch progress: {str(e)}")