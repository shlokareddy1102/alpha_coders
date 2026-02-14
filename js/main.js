document.getElementById("startBtn").addEventListener("click", function() {
    console.log("Frontend ready to connect to backend...");

    // Create modal for user role selection
    const modal = document.createElement("div");
    modal.id = "roleModal";
    modal.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.6);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 1000;
        backdrop-filter: blur(4px);
    `;

    const modalContent = document.createElement("div");
    modalContent.style.cssText = `
        background: white;
        padding: 50px;
        border-radius: 16px;
        text-align: center;
        max-width: 500px;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        animation: slideUp 0.3s ease-out;
    `;

    modalContent.innerHTML = `
        <h2 style="margin-bottom: 15px; color: #1F2937; font-size: 28px; font-weight: 700;">
            Select Your Role
        </h2>
        <p style="margin-bottom: 35px; color: #6B7280; font-size: 15px;">
            Choose how you want to use SkillMatch AI
        </p>
        <div style="display: flex; gap: 20px; justify-content: center;">
            <button id="coordinatorBtn" style="
                padding: 16px 28px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                border-radius: 10px;
                cursor: pointer;
                font-size: 16px;
                font-weight: 600;
                transition: all 0.3s;
                box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
            ">
                <i class="fa-solid fa-user-tie"></i> Placement Coordinator
            </button>
            <button id="recruiterBtn" style="
                padding: 16px 28px;
                background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                color: white;
                border: none;
                border-radius: 10px;
                cursor: pointer;
                font-size: 16px;
                font-weight: 600;
                transition: all 0.3s;
                box-shadow: 0 4px 15px rgba(245, 87, 108, 0.4);
            ">
                <i class="fa-solid fa-briefcase"></i> Recruiter
            </button>
        </div>
    `;

    modal.appendChild(modalContent);
    document.body.appendChild(modal);

    // Add hover effects
    document.getElementById("coordinatorBtn").addEventListener("mouseover", function() {
        this.style.transform = "translateY(-2px)";
        this.style.boxShadow = "0 6px 20px rgba(102, 126, 234, 0.6)";
    });
    document.getElementById("coordinatorBtn").addEventListener("mouseout", function() {
        this.style.transform = "translateY(0)";
        this.style.boxShadow = "0 4px 15px rgba(102, 126, 234, 0.4)";
    });

    document.getElementById("recruiterBtn").addEventListener("mouseover", function() {
        this.style.transform = "translateY(-2px)";
        this.style.boxShadow = "0 6px 20px rgba(245, 87, 108, 0.6)";
    });
    document.getElementById("recruiterBtn").addEventListener("mouseout", function() {
        this.style.transform = "translateY(0)";
        this.style.boxShadow = "0 4px 15px rgba(245, 87, 108, 0.4)";
    });

    // Handle button clicks
    document.getElementById("coordinatorBtn").addEventListener("click", function() {
        console.log("Placement Coordinator selected");
        window.location.href = "coordinator.html";
    });

    document.getElementById("recruiterBtn").addEventListener("click", function() {
        console.log("Recruiter selected");
        window.location.href = "recruiter.html";
    });

    // Close modal when clicking outside
    modal.addEventListener("click", function(e) {
        if (e.target === modal) {
            modal.remove();
        }
    });
});

// Add CSS animation
const style = document.createElement('style');
style.textContent = `
    @keyframes slideUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
`;
document.head.appendChild(style);
