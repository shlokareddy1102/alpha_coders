document.addEventListener('DOMContentLoaded', () => {

    const statsGrid = {
        totalStudents: document.getElementById('totalStudents'),
        faissVectors: document.getElementById('faissVectors'),
        totalFiles: document.getElementById('totalFiles')
    };

    const studentListDiv = document.getElementById('studentList');
    const addModal = document.getElementById('addModal');
    const editModal = document.getElementById('editModal');
    const addStudentForm = document.getElementById('addStudentForm');
    const editStudentForm = document.getElementById('editStudentForm');
    const formMessage = document.getElementById('formMessage');
    const editMessage = document.getElementById('editMessage');
    const refreshBtn = document.getElementById('refreshBtn');
    const searchInput = document.getElementById('searchInput');
    const searchBtn = document.getElementById('searchBtn');
    const clearSearchBtn = document.getElementById('clearSearchBtn');

    // ================= SEARCH =================

    searchBtn.addEventListener('click', () => {
        const query = searchInput.value.trim().toLowerCase();
        loadStudents(query);
    });

    clearSearchBtn.addEventListener('click', () => {
        searchInput.value = '';
        loadStudents();
    });

    // ================= INITIAL LOAD =================

    loadStats();
    loadStudents();

    // ================= ADD STUDENT =================

    document.getElementById('addStudentBtn').addEventListener('click', () => {
        addModal.style.display = 'flex';
    });

    document.getElementById('closeModal').addEventListener('click', () => {
        addModal.style.display = 'none';
        addStudentForm.reset();
        formMessage.innerHTML = '';
    });

    window.addEventListener('click', (e) => {
        if (e.target === addModal) {
            addModal.style.display = 'none';
            addStudentForm.reset();
            formMessage.innerHTML = '';
        }
        if (e.target === editModal) {
            editModal.style.display = 'none';
            editMessage.innerHTML = '';
        }
    });

    addStudentForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        formMessage.innerHTML = '<p style="color: #4ECDC4;">Submitting...</p>';

        const formData = new FormData(addStudentForm);

        try {
            const response = await fetch('http://localhost:8000/add-student', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || 'Unknown error');
            }

            formMessage.innerHTML = `<p style="color: green;">✅ Student ${data.name} added successfully!</p>`;
            addStudentForm.reset();

            setTimeout(() => {
                addModal.style.display = 'none';
                formMessage.innerHTML = '';
                loadStats();
                loadStudents();
            }, 1500);

        } catch (error) {
            formMessage.innerHTML = `<p style="color: red;">${error.message}</p>`;
        }
    });

    // ================= LOAD STATS =================

    async function loadStats() {
        try {
            const res = await fetch('http://localhost:8000/stats');
            const data = await res.json();

            statsGrid.totalStudents.textContent = data.mongodb?.total_students || 0;
            statsGrid.faissVectors.textContent = data.faiss?.vectors || 0;
            statsGrid.totalFiles.textContent = data.storage?.total_files || 0;

        } catch (e) {
            console.error('Failed to load stats', e);
        }
    }

    // ================= LOAD STUDENTS =================

    async function loadStudents(searchQuery = '') {
        try {
            const res = await fetch('http://localhost:8000/students');
            const students = await res.json();

            let filtered = students;

            if (searchQuery) {
                filtered = students.filter(s =>
                    s.name.toLowerCase().includes(searchQuery)
                );
            }

            if (!filtered.length) {
                studentListDiv.innerHTML = `
                    <div class="card" style="text-align:center; padding:40px;">
                        No students found.
                    </div>`;
                return;
            }

            let html = '<div class="candidates-grid">';

            filtered.forEach(s => {
                html += `
                    <div class="candidate-card">
                        <h3>${s.name}</h3>
                        <p>${s.branch} · Year ${s.year}</p>
                        <p><strong>Skills:</strong> ${s.skills.join(', ')}</p>

                        <div style="margin-top:15px; display:flex; gap:10px;">
                            <button onclick="editStudent('${s.student_id}')" 
                                style="background:#4ECDC4; border:none; padding:6px 12px; border-radius:6px; color:white; cursor:pointer;">
                                Edit
                            </button>

                            <button onclick="deleteStudent('${s.student_id}')" 
                                style="background:#dc2626; border:none; padding:6px 12px; border-radius:6px; color:white; cursor:pointer;">
                                Delete
                            </button>

                            <a href="http://localhost:8000${s.resume?.file_url}" target="_blank"
                                style="background:#374151; padding:6px 12px; border-radius:6px; color:white; text-decoration:none;">
                                Resume
                            </a>
                        </div>
                    </div>
                `;
            });

            html += '</div>';
            studentListDiv.innerHTML = html;

        } catch (e) {
            console.error(e);
            studentListDiv.innerHTML = '<div style="color:red;">Error loading students</div>';
        }
    }

    // ================= EDIT STUDENT =================

    window.editStudent = async (studentId) => {
        try {
            const res = await fetch(`http://localhost:8000/student/${studentId}`);
            const student = await res.json();

            if (!res.ok) throw new Error(student.detail);

            document.getElementById('editStudentId').value = student.student_id;
            document.getElementById('editSkills').value = student.skills.join(', ');

            editMessage.innerHTML = '';
            editModal.style.display = 'flex';

        } catch (error) {
            alert('Failed to load student data: ' + error.message);
        }
    };

    editStudentForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        editMessage.innerHTML = '<p style="color:#4ECDC4;">Updating...</p>';

        const studentId = document.getElementById('editStudentId').value;
        const skills = document.getElementById('editSkills').value.trim();

        const formData = new FormData();
        formData.append('skills', skills);

        try {
            const response = await fetch(`http://localhost:8000/student/${studentId}`, {
                method: 'PUT',
                body: formData
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || "Update failed");
            }

            editMessage.innerHTML = '<p style="color:green;">Updated successfully</p>';

            setTimeout(() => {
                editModal.style.display = 'none';
                loadStudents();
            }, 1200);

        } catch (error) {
            editMessage.innerHTML = `<p style="color:red;">${error.message}</p>`;
        }
    });

    // ================= DELETE STUDENT =================

    window.deleteStudent = async (studentId) => {
        if (!confirm('Are you sure you want to delete this student? This action cannot be undone.')) return;

        try {
            const res = await fetch(`http://localhost:8000/student/${studentId}`, { method: 'DELETE' });

            if (!res.ok) {
                const err = await res.json();
                throw new Error(err.detail || 'Delete failed');
            }

            loadStudents();
            loadStats();

        } catch (e) {
            alert('Delete failed: ' + e.message);
        }
    };

});
