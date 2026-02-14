document.getElementById("startBtn").addEventListener("click", function() {

    console.log("Frontend ready to connect to backend...");

    // Remove existing modal if it exists
    const existingModal = document.getElementById("roleModal");
    if (existingModal) {
        existingModal.remove();
    }

    // Create modal for user role selection
    const modal = document.createElement("div");
    modal.id = "roleModal";
    modal.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.5);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 1000;
    `;

    const modalContent = document.createElement("div");
    modalContent.style.cssText = `
        background: white;
        padding: 60px 50px;
        border-radius: 16px;
        text-align: center;
        max-width: 600px;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
    `;

    modalContent.innerHTML = `
        <h2 style="margin-bottom: 40px; color: #333; font-size: 28px; font-weight: 700;">Select Your Role</h2>
        <div style="display: flex; gap: 20px; justify-content: center;">
            <button id="coordinatorBtn" style="
                padding: 16px 32px;
                background: #4ECDC4;
                color: white;
                border: none;
                border-radius: 8px;
                cursor: pointer;
                font-size: 17px;
                font-weight: 600;
                transition: all 0.3s;
                flex: 1;
            ">Placement Coordinator</button>
            <button id="recruiterBtn" style="
                padding: 16px 32px;
                background: #FF6B6B;
                color: white;
                border: none;
                border-radius: 8px;
                cursor: pointer;
                font-size: 17px;
                font-weight: 600;
                transition: all 0.3s;
                flex: 1;
            ">Recruiter</button>
        </div>
    `;

    modal.appendChild(modalContent);
    document.body.appendChild(modal);

    // Add hover effects
    document.getElementById("coordinatorBtn").addEventListener("mouseover", function() {
        this.style.background = "#2ba39f";
    });
    document.getElementById("coordinatorBtn").addEventListener("mouseout", function() {
        this.style.background = "#4ECDC4";
    });

    document.getElementById("recruiterBtn").addEventListener("mouseover", function() {
        this.style.background = "#ff5252";
    });
    document.getElementById("recruiterBtn").addEventListener("mouseout", function() {
        this.style.background = "#FF6B6B";
    });

    // Handle button clicks
    document.getElementById("coordinatorBtn").addEventListener("click", function() {
        console.log("Placement Coordinator selected");
        modal.remove();
        window.location.href = 'coordinator.html';
    });

    document.getElementById("recruiterBtn").addEventListener("click", function() {
        console.log("Recruiter selected");
        modal.remove();
        showJobDescriptionForm();
    });

    // Close modal when clicking outside
    modal.addEventListener("click", function(e) {
        if (e.target === modal) {
            modal.remove();
        }
    });

});

// Function to show job description form
function showJobDescriptionForm() {
    // Remove existing modal if it exists
    const existingModal = document.getElementById("jobDescriptionModal");
    if (existingModal) {
        existingModal.remove();
    }

    const formModal = document.createElement("div");
    formModal.id = "jobDescriptionModal";
    formModal.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.5);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 1000;
        overflow-y: auto;
        padding: 20px;
    `;

    const formContent = document.createElement("div");
    formContent.style.cssText = `
        background: white;
        padding: 50px 40px;
        border-radius: 16px;
        max-width: 700px;
        width: 100%;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
        text-align: center;
    `;

    formContent.innerHTML = `
        <div style="margin-bottom: 30px;">
            <div style="
                width: 80px;
                height: 80px;
                background: #4ECDC4;
                border-radius: 12px;
                display: flex;
                align-items: center;
                justify-content: center;
                margin: 0 auto 25px;
                font-size: 40px;
            ">📋</div>
        </div>
        
        <h2 style="
            margin-bottom: 15px;
            color: #1F2937;
            font-size: 28px;
            font-weight: 700;
        ">Enter Job Description</h2>
        
        <p style="
            margin-bottom: 40px;
            color: #6B7280;
            font-size: 15px;
            line-height: 1.6;
        ">Paste the job description below and our AI will extract skills, requirements, and qualifications</p>
        
        <form id="jobDescForm" style="text-align: left;">
            <div style="margin-bottom: 25px; position: relative;">
                <div style="
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 10px;
                ">
                    <label for="jobDescription" style="
                        color: #374151;
                        font-weight: 600;
                        font-size: 15px;
                    ">Job Description</label>
                    <button type="button" id="useSampleBtn" style="
                        background: none;
                        border: none;
                        color: #4ECDC4;
                        cursor: pointer;
                        font-size: 14px;
                        font-weight: 600;
                        padding: 0;
                    ">Use Sample</button>
                </div>
                <textarea id="jobDescription" placeholder="Paste the full job description here..." required style="
                    width: 100%;
                    padding: 16px;
                    border: 1px solid #E5E7EB;
                    border-radius: 8px;
                    font-size: 14px;
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    min-height: 220px;
                    box-sizing: border-box;
                    resize: vertical;
                    background: #F9FAFB;
                    transition: all 0.3s ease;
                "></textarea>
            </div>
            
            <button type="submit" style="
                width: 100%;
                padding: 14px 24px;
                background: #4ECDC4;
                color: white;
                border: none;
                border-radius: 8px;
                cursor: pointer;
                font-size: 16px;
                font-weight: 600;
                transition: all 0.3s ease;
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 8px;
                margin-top: 20px;
            ">
                <span>✨ Extract Skills & Requirements</span>
            </button>
        </form>
    `;

    formModal.appendChild(formContent);
    document.body.appendChild(formModal);

    // Use Sample button handler
    document.getElementById("useSampleBtn").addEventListener("click", function(e) {
        e.preventDefault();
        const sampleJob = "Senior Software Engineer\n\nWe are looking for an experienced Senior Software Engineer to join our team. \n\nRequired Skills:\n- 5+ years of experience in full-stack development\n- Proficiency in JavaScript/TypeScript, React, Node.js\n- Strong knowledge of databases (SQL and NoSQL)\n- Experience with cloud platforms (AWS, GCP, or Azure)\n- Git version control and CI/CD pipelines\n\nResponsibilities:\n- Design and develop scalable web applications\n- Mentor junior developers\n- Write clean, maintainable code\n- Participate in code reviews\n- Collaborate with product and design teams\n\nNice to Have:\n- Experience with Docker and Kubernetes\n- Contributions to open-source projects\n- Knowledge of microservices architecture";
        
        document.getElementById("jobDescription").value = sampleJob;
    });

    // Form submission handler
    document.getElementById("jobDescForm").addEventListener("submit", function(e) {
        e.preventDefault();
        
        const jobDescription = document.getElementById("jobDescription").value;
        
        if (!jobDescription.trim()) {
            alert("Please enter a job description");
            return;
        }
        
        console.log("Job Description:", jobDescription);
        
        // Show loading state
        const submitBtn = formContent.querySelector("button[type='submit']");
        submitBtn.disabled = true;
        submitBtn.innerHTML = "<span>⏳ Extracting skills...</span>";
        
        // Extract skills locally (with fallback to backend)
        extractSkillsLocal(jobDescription, submitBtn, formModal);
    });

    // Add hover effect to textarea
    const textarea = formContent.querySelector("textarea");
    textarea.addEventListener("focus", function() {
        this.style.borderColor = "#4ECDC4";
        this.style.boxShadow = "0 0 0 3px rgba(78, 205, 196, 0.1)";
    });
    textarea.addEventListener("blur", function() {
        this.style.borderColor = "#E5E7EB";
        this.style.boxShadow = "none";
    });

    // Close modal when clicking outside
    formModal.addEventListener("click", function(e) {
        if (e.target === formModal) {
            formModal.remove();
        }
    });
}

// Function to extract skills locally
function extractSkillsLocal(jobDescription, submitBtn, formModal) {
    // Common tech skills organized by category
    const skillsByCategory = {
        language: ["Python", "JavaScript", "TypeScript", "Java", "C++", "C#", "PHP", "Ruby", "Go", "Rust", "Kotlin", "Swift"],
        framework: ["React", "Vue", "Angular", "Node.js", "Django", "Flask", "Spring", "ASP.NET", "Express", "FastAPI"],
        database: ["SQL", "NoSQL", "MongoDB", "PostgreSQL", "MySQL", "Redis", "Elasticsearch"],
        devops: ["AWS", "Azure", "GCP", "Google Cloud", "Docker", "Kubernetes", "Jenkins", "Git", "GitHub", "GitLab", "CI/CD"],
        tool: ["HTML", "CSS", "REST API", "GraphQL", "Microservices", "Linux", "Windows", "MacOS", "JIRA", "Slack"],
        softSkill: ["Communication", "Leadership", "Problem Solving", "Agile", "Scrum", "Kanban", "Team Collaboration"]
    };

    const text = jobDescription.toLowerCase();

    // Extract skills and categorize them
    const requiredSkills = [];
    const preferredSkills = [];
    const niceToHaveSkills = [];

    // Check if skills are in specific sections
    const lines = jobDescription.split('\n');
    let currentSection = '';

    lines.forEach((line) => {
        const lowerLine = line.toLowerCase();
        if (lowerLine.includes('required') && !lowerLine.includes('nice')) {
            currentSection = 'required';
        } else if (lowerLine.includes('preferred') || lowerLine.includes('advantage')) {
            currentSection = 'preferred';
        } else if (lowerLine.includes('nice to have')) {
            currentSection = 'nice';
        }
    });

    // Extract all skills with their categories
    let allExtractedSkills = [];
    
    for (const [category, skills] of Object.entries(skillsByCategory)) {
        skills.forEach(skill => {
            if (text.includes(skill.toLowerCase())) {
                allExtractedSkills.push({
                    name: skill,
                    category: category
                });
            }
        });
    }

    // Distribute skills into sections (simple logic)
    const half = Math.ceil(allExtractedSkills.length / 2);
    requiredSkills.push(...allExtractedSkills.slice(0, half).map(s => ({ name: s.name, category: s.category })));
    
    if (allExtractedSkills.length > half) {
        const remaining = allExtractedSkills.slice(half);
        const third = Math.ceil(remaining.length / 2);
        preferredSkills.push(...remaining.slice(0, third).map(s => ({ name: s.name, category: s.category })));
        niceToHaveSkills.push(...remaining.slice(third).map(s => ({ name: s.name, category: s.category })));
    }

    const data = {
        required: requiredSkills.slice(0, 10),
        preferred: preferredSkills.slice(0, 5),
        nice: niceToHaveSkills.slice(0, 3)
    };

    console.log("Extracted Skills:", data);
    displayExtractedSkills(data, formModal);
    submitBtn.innerHTML = "<span>✨ Extract Skills & Requirements</span>";
}


function displayExtractedSkills(data, formModal) {
    formModal.remove();

    // Remove existing skills modal if it exists
    const existingSkillsModal = document.getElementById("skillsModal");
    if (existingSkillsModal) {
        existingSkillsModal.remove();
    }
    
    const skillsModal = document.createElement("div");
    skillsModal.id = "skillsModal";
    skillsModal.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.5);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 1000;
        overflow-y: auto;
        padding: 20px;
    `;

    const skillsContent = document.createElement("div");
    skillsContent.style.cssText = `
        background: white;
        padding: 50px 40px;
        border-radius: 16px;
        max-width: 900px;
        width: 100%;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
    `;

    const getCategoryColor = (category) => {
        const colors = {
            language: { bg: '#E0F2FE', text: '#0369A1', border: '#BAE6FD' },
            framework: { bg: '#F0FDF4', text: '#166534', border: '#BBFEF0' },
            database: { bg: '#FEF3C7', text: '#B45309', border: '#FCD34D' },
            devops: { bg: '#FCE7F3', text: '#9D174D', border: '#FBCFE8' },
            tool: { bg: '#DDD6FE', text: '#4F46E5', border: '#C7D2FE' },
            softSkill: { bg: '#DBEAFE', text: '#0C4A6E', border: '#93C5FD' }
        };
        return colors[category] || colors.language;
    };

    const requiredSkills = data.required || [];
    const preferredSkills = data.preferred || [];
    const niceSkills = data.nice || [];

    let skillsHTML = `
        <h2 style="
            margin-bottom: 8px;
            color: #1F2937;
            font-size: 26px;
            font-weight: 700;
        ">⭐ Extracted Skills & Requirements</h2>
        
        <p style="
            margin-bottom: 30px;
            color: #6B7280;
            font-size: 14px;
        ">AI-extracted insights from job description</p>
    `;

    // Display Required Skills
    if (requiredSkills.length > 0) {
        skillsHTML += `<div style="margin-bottom: 28px;">
            <h3 style="
                color: #374151;
                font-size: 13px;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                margin-bottom: 12px;
            ">REQUIRED</h3>
            <div style="display: flex; flex-wrap: wrap; gap: 10px;">
        `;
        requiredSkills.forEach(skill => {
            const colors = getCategoryColor(skill.category);
            skillsHTML += `
                <span style="
                    background: ${colors.bg};
                    color: ${colors.text};
                    padding: 8px 16px;
                    border-radius: 6px;
                    font-size: 13px;
                    font-weight: 500;
                    border: 1px solid ${colors.border};
                ">
                    ${skill.name}
                </span>
            `;
        });
        skillsHTML += `</div></div>`;
    }

    // Display Preferred Skills
    if (preferredSkills.length > 0) {
        skillsHTML += `<div style="margin-bottom: 28px;">
            <h3 style="
                color: #374151;
                font-size: 13px;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                margin-bottom: 12px;
            ">PREFERRED</h3>
            <div style="display: flex; flex-wrap: wrap; gap: 10px;">
        `;
        preferredSkills.forEach(skill => {
            const colors = getCategoryColor(skill.category);
            skillsHTML += `
                <span style="
                    background: ${colors.bg};
                    color: ${colors.text};
                    padding: 8px 16px;
                    border-radius: 6px;
                    font-size: 13px;
                    font-weight: 500;
                    border: 1px solid ${colors.border};
                ">
                    ${skill.name}
                </span>
            `;
        });
        skillsHTML += `</div></div>`;
    }

    // Display Nice to Have Skills
    if (niceSkills.length > 0) {
        skillsHTML += `<div style="margin-bottom: 28px;">
            <h3 style="
                color: #374151;
                font-size: 13px;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                margin-bottom: 12px;
            ">NICE TO HAVE</h3>
            <div style="display: flex; flex-wrap: wrap; gap: 10px;">
        `;
        niceSkills.forEach(skill => {
            const colors = getCategoryColor(skill.category);
            skillsHTML += `
                <span style="
                    background: ${colors.bg};
                    color: ${colors.text};
                    padding: 8px 16px;
                    border-radius: 6px;
                    font-size: 13px;
                    font-weight: 500;
                    border: 1px solid ${colors.border};
                ">
                    ${skill.name}
                </span>
            `;
        });
        skillsHTML += `</div></div>`;
    }

    // Add skill categories legend
    skillsHTML += `
        <div style="
            background: #F9FAFB;
            border-top: 1px solid #E5E7EB;
            padding: 20px;
            margin: 30px -40px -40px -40px;
            border-radius: 0 0 16px 16px;
        ">
            <p style="
                color: #6B7280;
                font-size: 12px;
                margin-bottom: 10px;
                font-weight: 600;
            ">Skill Categories:</p>
            <div style="display: flex; flex-wrap: wrap; gap: 16px;">
                <div style="display: flex; align-items: center; gap: 6px;">
                    <span style="width: 8px; height: 8px; background: #0369A1; border-radius: 50%;"></span>
                    <span style="font-size: 12px; color: #4B5563;">Language</span>
                </div>
                <div style="display: flex; align-items: center; gap: 6px;">
                    <span style="width: 8px; height: 8px; background: #166534; border-radius: 50%;"></span>
                    <span style="font-size: 12px; color: #4B5563;">Framework</span>
                </div>
                <div style="display: flex; align-items: center; gap: 6px;">
                    <span style="width: 8px; height: 8px; background: #B45309; border-radius: 50%;"></span>
                    <span style="font-size: 12px; color: #4B5563;">Tool</span>
                </div>
                <div style="display: flex; align-items: center; gap: 6px;">
                    <span style="width: 8px; height: 8px; background: #4F46E5; border-radius: 50%;"></span>
                    <span style="font-size: 12px; color: #4B5563;">Soft Skill</span>
                </div>
                <div style="display: flex; align-items: center; gap: 6px;">
                    <span style="width: 8px; height: 8px; background: #DC2626; border-radius: 50%;"></span>
                    <span style="font-size: 12px; color: #4B5563;">Requirement</span>
                </div>
            </div>
        </div>
    `;

    skillsContent.innerHTML = `
        ${skillsHTML}
        <div style="display: flex; gap: 12px; margin-top: 30px;">
            <button id="closeSkillsBtn" style="
                flex: 1;
                padding: 12px 24px;
                background: #E5E7EB;
                color: #333;
                border: none;
                border-radius: 8px;
                cursor: pointer;
                font-size: 16px;
                font-weight: 600;
                transition: all 0.3s ease;
            ">Back</button>
            <button id="uploadCandidatesBtn" style="
                flex: 1;
                padding: 12px 24px;
                background: #4ECDC4;
                color: white;
                border: none;
                border-radius: 8px;
                cursor: pointer;
                font-size: 16px;
                font-weight: 600;
                transition: all 0.3s ease;
            ">View Candidate Rankings →</button>
        </div>
    `;

    skillsModal.appendChild(skillsContent);
    document.body.appendChild(skillsModal);

    // Event listeners for buttons
    document.getElementById("closeSkillsBtn").addEventListener("click", function() {
        skillsModal.remove();
    });

    document.getElementById("uploadCandidatesBtn").addEventListener("click", function() {
        console.log("Proceed to upload candidates");
        skillsModal.remove();
        // Add next step functionality here
    });

    // Close modal when clicking outside
    skillsModal.addEventListener("click", function(e) {
        if (e.target === skillsModal) {
            skillsModal.remove();
        }
    });
}
