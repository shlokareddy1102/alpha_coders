import os
import faiss
import numpy as np
from threading import Lock
from datetime import datetime

DIMENSION = 384
INDEX_FILE = "students.index"
index = None
index_lock = Lock()

# Monitoring stats
faiss_stats = {
    "last_rebuild": None,
    "add_failures": 0,
    "remove_failures": 0,
    "search_count": 0
}

def load_or_rebuild(student_records):
    """Load FAISS index from disk or rebuild from database"""
    global index
    with index_lock:
        if os.path.exists(INDEX_FILE):
            try:
                index = faiss.read_index(INDEX_FILE)
                print(f"Loaded FAISS index from file ({index.ntotal} students).")
                return True
            except Exception as e:
                print(f"Index corrupted ({e}). Rebuilding...")
        
        return _rebuild_index_unsafe(student_records)

def _rebuild_index_unsafe(student_records):
    """Rebuild index - MUST be called with lock held"""
    global index, faiss_stats
    
    try:
        base = faiss.IndexFlatIP(DIMENSION)
        index = faiss.IndexIDMap(base)
        
        if student_records:
            vectors = []
            ids = []
            for student in student_records:
                vectors.append(student["embedding"])
                ids.append(student["id"])
            
            vectors = np.array(vectors).astype("float32")
            faiss.normalize_L2(vectors)
            index.add_with_ids(vectors, np.array(ids))
        
        save_index()
        faiss_stats["last_rebuild"] = datetime.now()
        print(f"FAISS rebuilt from DB ({index.ntotal} students).")
        return True
        
    except Exception as e:
        print(f"Failed to rebuild FAISS: {e}")
        return False

def save_index():
    """Atomically save index to disk"""
    global index
    temp_file = INDEX_FILE + ".tmp"
    faiss.write_index(index, temp_file)
    os.replace(temp_file, INDEX_FILE)

def add_or_update_vector(student_id, embedding):
    """Add or update student vector in FAISS"""
    global index, faiss_stats
    
    # 🔴 FIX 1: Check if index initialized
    if index is None:
        raise RuntimeError("FAISS index not initialized. Call load_or_rebuild() first.")
    
    with index_lock:
        try:
            # 🟡 FIX 2: Removed unnecessary try-except
            # FAISS remove_ids() is safe even if ID doesn't exist
            index.remove_ids(np.array([student_id]))
            
            # Add new vector
            vector = np.array([embedding]).astype("float32")
            faiss.normalize_L2(vector)
            index.add_with_ids(vector, np.array([student_id]))
            save_index()
            return True
            
        except Exception as e:
            faiss_stats["add_failures"] += 1
            print(f"FAISS update failed for student {student_id}: {e}")
            return False

def remove_vector(student_id):
    """Remove student vector from FAISS"""
    global index, faiss_stats
    
    # 🔴 FIX 1: Check if index initialized
    if index is None:
        raise RuntimeError("FAISS index not initialized. Call load_or_rebuild() first.")
    
    with index_lock:
        try:
            # 🟡 FIX 2: Direct call without nested try-except
            index.remove_ids(np.array([student_id]))
            save_index()
            return True
        except Exception as e:
            faiss_stats["remove_failures"] += 1
            print(f"FAISS remove failed for student {student_id}: {e}")
            return False

def match(jd_embedding, top_k=10):
    """Find top K matching students for JD"""
    global index, faiss_stats
    
    # 🔴 FIX 1: Check if index initialized
    if index is None:
        raise RuntimeError("FAISS index not initialized. Call load_or_rebuild() first.")
    
    with index_lock:
        if index.ntotal == 0:
            return []
        
        top_k = min(top_k, index.ntotal)
        vector = np.array([jd_embedding]).astype("float32")
        faiss.normalize_L2(vector)
        
        scores, ids = index.search(vector, top_k)
        faiss_stats["search_count"] += 1
        
        results = []
        for score, sid in zip(scores[0], ids[0]):
            if sid == -1:
                continue
            results.append({
                "student_id": int(sid),
                "score": float(score)
            })
        return results

def get_stats():
    """Get FAISS statistics"""
    global index, faiss_stats
    
    # 🟡 FIX 3: Calculate total_students dynamically (removed from faiss_stats dict)
    with index_lock:
        stats = faiss_stats.copy()
        stats["total_students"] = index.ntotal if index else 0
        return stats

def force_rebuild_from_db(student_records):
    """Emergency rebuild - use if FAISS corrupted"""
    print("🚨 Force rebuilding FAISS from database...")
    with index_lock:
        success = _rebuild_index_unsafe(student_records)
    if success:
        print("✅ Rebuild successful!")
    else:
        print("❌ Rebuild failed!")
    return success