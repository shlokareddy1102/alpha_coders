from sentence_transformers import SentenceTransformer
from db import save_student, remove_student, get_all_students
from vector_engine import add_or_update_vector, remove_vector, match
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Lazy load model
_model = None

def get_model():
    global _model
    if _model is None:
        logger.info("Loading SentenceTransformer model...")
        _model = SentenceTransformer("all-MiniLM-L6-v2")
        logger.info("Model loaded successfully.")
    return _model

def register_student(student_id, summary):
    """Register or update student profile"""
    # Validation
    if not isinstance(student_id, int) or student_id <= 0:
        raise ValueError("student_id must be a positive integer")
    
    if not summary or not isinstance(summary, str):
        raise ValueError("summary must be a non-empty string")
    
    if len(summary.strip()) < 10:
        raise ValueError("summary too short (minimum 10 characters)")
    
    try:
        # Generate embedding
        model = get_model()
        embedding = model.encode(summary).tolist()
        
        # Save to database (source of truth)
        save_student(student_id, summary, embedding)
        
        # Update FAISS
        faiss_success = add_or_update_vector(student_id, embedding)
        
        if not faiss_success:
            # Rollback database
            logger.error(f"FAISS update failed for student {student_id}, rolling back...")
            remove_student(student_id)
            raise Exception("FAISS update failed, transaction rolled back")
        
        logger.info(f"✅ Student {student_id} registered/updated successfully.")
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to register student {student_id}: {e}")
        raise

def delete_student(student_id):
    """Delete student from system"""
    if not isinstance(student_id, int) or student_id <= 0:
        raise ValueError("student_id must be a positive integer")
    
    try:
        # Remove from database
        remove_student(student_id)
        
        # Remove from FAISS (less critical if fails)
        faiss_success = remove_vector(student_id)
        
        if not faiss_success:
            logger.warning(f"Student {student_id} removed from DB but FAISS cleanup failed")
        else:
            logger.info(f"✅ Student {student_id} deleted successfully.")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to delete student {student_id}: {e}")
        raise

def match_jd(jd_text, top_k=10):
    """Match students to job description"""
    # Validation
    if not jd_text or not isinstance(jd_text, str):
        raise ValueError("jd_text must be a non-empty string")
    
    if len(jd_text.strip()) < 20:
        raise ValueError("JD too short (minimum 20 characters)")
    
    try:
        # Generate embedding
        model = get_model()
        jd_embedding = model.encode(jd_text).tolist()
        
        # Search FAISS
        results = match(jd_embedding, top_k=top_k)
        
        if not results:
            logger.info("No matching students found for this JD.")
        else:
            logger.info(f"Found {len(results)} matching students.")
        
        return results
        
    except Exception as e:
        logger.error(f"Error matching JD: {e}")
        raise