/**
 * AI-Powered CV Generator - Frontend JavaScript
 */

class CVGenerator {
    constructor() {
        this.currentCVData = null;
        this.currentTemplate = 'professional';
        this.experienceCount = 0;
        this.projectCount = 0;
        this.certificationCount = 0;
        this.educationCount = 0;
        this.init();
    }

    init() {
        this.bindEvents();
        this.loadSampleData();
        this.loadTrainingInfo();
    }

    bindEvents() {
        // Form submission
        document.getElementById('cvForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.generateCV();
        });

        // CSV upload
        document.getElementById('uploadCsvBtn').addEventListener('click', () => {
            document.getElementById('csvFileInput').click();
        });

        document.getElementById('csvFileInput').addEventListener('change', (e) => {
            this.handleCsvUpload(e);
        });



        // Download PDF
        document.getElementById('downloadPdfBtn').addEventListener('click', () => {
            this.downloadPDF();
        });

        // Dynamic sections
        document.getElementById('addExperienceBtn').addEventListener('click', () => {
            this.addExperienceItem();
        });

        document.getElementById('addProjectBtn').addEventListener('click', () => {
            this.addProjectItem();
        });

        document.getElementById('addCertificationBtn').addEventListener('click', () => {
            this.addCertificationItem();
        });

        // Generate summary with fine-tuned AI
        document.getElementById('generateSummaryBtn').addEventListener('click', () => {
            this.generateSummary();
        });

        // Test API key
        document.getElementById('testApiBtn').addEventListener('click', () => {
            this.testApiKey();
        });

        // Generate ATS keywords
        document.getElementById('generateAtsKeywordsBtn').addEventListener('click', () => {
            this.generateAtsKeywords();
        });

        // Add selected keywords to skills
        document.getElementById('addSelectedKeywordsBtn').addEventListener('click', () => {
            this.addSelectedKeywords();
        });

        // Clear ATS keywords
        document.getElementById('clearKeywordsBtn').addEventListener('click', () => {
            this.clearAtsKeywords();
        });

        document.getElementById('addProjectBtn').addEventListener('click', () => {
            this.addProjectItem();
        });

        document.getElementById('addCertificationBtn').addEventListener('click', () => {
            this.addCertificationItem();
        });

        // Real-time form updates
        this.bindFormUpdates();
    }

    bindFormUpdates() {
        const form = document.getElementById('cvForm');

        // Use event delegation for dynamic elements
        form.addEventListener('input', (e) => {
            if (e.target.matches('input, textarea, select')) {
                this.updateLivePreview();
            }
        });
    }

    addExperienceItem() {
        this.experienceCount++;
        const container = document.getElementById('experienceContainer');
        const emptyState = document.getElementById('experienceEmptyState');

        const experienceHTML = `
            <div class="experience-item" data-index="${this.experienceCount}">
                <h4>
                    Experience ${this.experienceCount}
                    <button type="button" class="remove-btn" onclick="cvGenerator.removeExperienceItem(${this.experienceCount})">
                        <i class="fas fa-trash"></i> Remove
                    </button>
                </h4>
                <div class="form-row">
                    <div class="form-group">
                        <label for="experience_${this.experienceCount}_title">Job Title</label>
                        <input type="text" id="experience_${this.experienceCount}_title" name="experience_${this.experienceCount}_title" placeholder="Software Engineer">
                    </div>
                    <div class="form-group">
                        <label for="experience_${this.experienceCount}_company">Company</label>
                        <input type="text" id="experience_${this.experienceCount}_company" name="experience_${this.experienceCount}_company" placeholder="Company Name">
                    </div>
                </div>
                <div class="form-row">
                    <div class="form-group">
                        <label for="experience_${this.experienceCount}_start">Start Date</label>
                        <input type="text" id="experience_${this.experienceCount}_start" name="experience_${this.experienceCount}_start" placeholder="2022-01">
                    </div>
                    <div class="form-group">
                        <label for="experience_${this.experienceCount}_end">End Date</label>
                        <input type="text" id="experience_${this.experienceCount}_end" name="experience_${this.experienceCount}_end" placeholder="Present">
                    </div>
                </div>
                <div class="responsibilities-container" id="responsibilities_${this.experienceCount}">
                    <label>Responsibilities</label>
                    <div class="responsibility-item">
                        <textarea name="experience_${this.experienceCount}_resp_1" rows="2" placeholder="Key responsibility or achievement..."></textarea>
                        <button type="button" class="remove-btn" onclick="cvGenerator.removeResponsibility(this)">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                </div>
                <button type="button" class="add-responsibility-btn" onclick="cvGenerator.addResponsibility(${this.experienceCount})">
                    <i class="fas fa-plus"></i> Add Responsibility
                </button>
            </div>
        `;

        container.insertAdjacentHTML('beforeend', experienceHTML);
        emptyState.classList.add('hidden');

        // Focus on the first input of the new experience
        setTimeout(() => {
            document.getElementById(`experience_${this.experienceCount}_title`).focus();
        }, 100);
    }

    removeExperienceItem(index) {
        const item = document.querySelector(`[data-index="${index}"]`);
        if (item) {
            item.remove();

            // Show empty state if no experiences left
            const container = document.getElementById('experienceContainer');
            const emptyState = document.getElementById('experienceEmptyState');

            if (container.children.length === 0) {
                emptyState.classList.remove('hidden');
            }
        }
    }

    addResponsibility(experienceIndex) {
        const container = document.getElementById(`responsibilities_${experienceIndex}`);
        const existingResponsibilities = container.querySelectorAll('.responsibility-item');
        const respIndex = existingResponsibilities.length + 1;

        const responsibilityHTML = `
            <div class="responsibility-item">
                <textarea name="experience_${experienceIndex}_resp_${respIndex}" rows="2" placeholder="Key responsibility or achievement..."></textarea>
                <button type="button" class="remove-btn" onclick="cvGenerator.removeResponsibility(this)">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        `;

        container.insertAdjacentHTML('beforeend', responsibilityHTML);
    }

    removeResponsibility(button) {
        const responsibilityItem = button.closest('.responsibility-item');
        const container = responsibilityItem.closest('.responsibilities-container');

        // Don't remove if it's the last responsibility
        if (container.querySelectorAll('.responsibility-item').length > 1) {
            responsibilityItem.remove();
        } else {
            this.showToast('At least one responsibility is required', 'warning');
        }
    }

    addProjectItem() {
        this.projectCount++;
        const container = document.getElementById('projectContainer');
        const emptyState = document.getElementById('projectEmptyState');

        const projectHTML = `
            <div class="project-item" data-index="${this.projectCount}">
                <h4>
                    Project ${this.projectCount}
                    <button type="button" class="remove-btn" onclick="cvGenerator.removeProjectItem(${this.projectCount})">
                        <i class="fas fa-trash"></i> Remove
                    </button>
                </h4>
                <div class="form-row">
                    <div class="form-group">
                        <label for="project_${this.projectCount}_title">Project Title</label>
                        <input type="text" id="project_${this.projectCount}_title" name="project_${this.projectCount}_title" placeholder="E-commerce Platform">
                    </div>
                    <div class="form-group">
                        <label for="project_${this.projectCount}_github">GitHub URL</label>
                        <input type="url" id="project_${this.projectCount}_github" name="project_${this.projectCount}_github" placeholder="https://github.com/username/project">
                    </div>
                </div>
                <div class="form-group">
                    <label for="project_${this.projectCount}_description">Description</label>
                    <textarea id="project_${this.projectCount}_description" name="project_${this.projectCount}_description" rows="2" placeholder="Brief project description..."></textarea>
                </div>
                <div class="form-group">
                    <label for="project_${this.projectCount}_technologies">Technologies Used</label>
                    <input type="text" id="project_${this.projectCount}_technologies" name="project_${this.projectCount}_technologies" placeholder="React, Node.js, MongoDB">
                    <small>Separate technologies with commas</small>
                </div>
            </div>
        `;

        container.insertAdjacentHTML('beforeend', projectHTML);
        emptyState.classList.add('hidden');

        // Focus on the first input of the new project
        setTimeout(() => {
            document.getElementById(`project_${this.projectCount}_title`).focus();
        }, 100);
    }

    removeProjectItem(index) {
        const item = document.querySelector(`.project-item[data-index="${index}"]`);
        if (item) {
            item.remove();

            // Show empty state if no projects left
            const container = document.getElementById('projectContainer');
            const emptyState = document.getElementById('projectEmptyState');

            if (container.children.length === 0) {
                emptyState.classList.remove('hidden');
            }
        }
    }

    addCertificationItem() {
        this.certificationCount++;
        const container = document.getElementById('certificationContainer');
        const emptyState = document.getElementById('certificationEmptyState');

        const certificationHTML = `
            <div class="certification-item" data-index="${this.certificationCount}">
                <h4>
                    Certification ${this.certificationCount}
                    <button type="button" class="remove-btn" onclick="cvGenerator.removeCertificationItem(${this.certificationCount})">
                        <i class="fas fa-trash"></i> Remove
                    </button>
                </h4>
                <div class="form-row">
                    <div class="form-group">
                        <label for="cert_${this.certificationCount}_name">Certification Name</label>
                        <input type="text" id="cert_${this.certificationCount}_name" name="cert_${this.certificationCount}_name" placeholder="AWS Certified Developer">
                    </div>
                    <div class="form-group">
                        <label for="cert_${this.certificationCount}_issuer">Issuer</label>
                        <input type="text" id="cert_${this.certificationCount}_issuer" name="cert_${this.certificationCount}_issuer" placeholder="Amazon Web Services">
                    </div>
                    <div class="form-group">
                        <label for="cert_${this.certificationCount}_year">Year</label>
                        <input type="text" id="cert_${this.certificationCount}_year" name="cert_${this.certificationCount}_year" placeholder="2023">
                    </div>
                </div>
            </div>
        `;

        container.insertAdjacentHTML('beforeend', certificationHTML);
        emptyState.classList.add('hidden');

        // Focus on the first input of the new certification
        setTimeout(() => {
            document.getElementById(`cert_${this.certificationCount}_name`).focus();
        }, 100);
    }

    removeCertificationItem(index) {
        const item = document.querySelector(`.certification-item[data-index="${index}"]`);
        if (item) {
            item.remove();

            // Show empty state if no certifications left
            const container = document.getElementById('certificationContainer');
            const emptyState = document.getElementById('certificationEmptyState');

            if (container.children.length === 0) {
                emptyState.classList.remove('hidden');
            }
        }
    }





    async generateSummary() {
        console.log('Generate Summary clicked');
        const generateBtn = document.getElementById('generateSummaryBtn');
        const summaryTextarea = document.getElementById('summary');

        if (!generateBtn || !summaryTextarea) {
            console.error('Required elements not found:', { generateBtn, summaryTextarea });
            return;
        }

        // Get current form data to generate contextual summary
        const formData = this.getFormData();
        console.log('Form data for summary:', formData);

        // Check if we have enough data to generate a summary
        const hasExperience = Object.keys(formData).some(key => key.includes('experience') && key.includes('title') && formData[key]);
        if (!formData.name && !formData.skills_technical && !hasExperience) {
            console.log('Not enough data for summary. Available fields:', Object.keys(formData));
            this.showToast('Please fill in your name, skills, or experience first to generate a summary', 'warning');
            return;
        }

        generateBtn.disabled = true;
        generateBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Generating...';

        try {
            const response = await fetch('/api/generate-summary', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });

            const result = await response.json();
            console.log('Professional Summary API Response:', result);

            if (result.success) {
                console.log('Summary received:', result.summary);
                summaryTextarea.value = result.summary;
                console.log('Summary set in textarea:', summaryTextarea.value);
                this.showToast('Professional summary generated using fine-tuned model!', 'success');
            } else {
                throw new Error(result.error || 'Failed to generate summary');
            }
        } catch (error) {
            console.error('Error generating summary:', error);
            if (error.message.includes('DeepSeek API Error')) {
                this.showToast('DeepSeek API Error: Please check your API key and try again', 'error');
            } else {
                this.showToast('Error generating summary: ' + error.message, 'error');
            }
        } finally {
            generateBtn.disabled = false;
            generateBtn.innerHTML = '<i class="fas fa-magic"></i> Generate with AI';
        }
    }
    loadSampleData() {
        // No sample data - start with empty form
        console.log("Application initialized - ready for user input");
    }

    async loadTrainingInfo() {
        const trainingInfoDiv = document.getElementById('trainingInfo');

        try {
            const response = await fetch('/api/training-info');
            const result = await response.json();

            if (result.success) {
                trainingInfoDiv.innerHTML = `
                    <i class="fas fa-check-circle"></i>
                    ${result.message}
                `;
                trainingInfoDiv.classList.add('success');
            } else {
                trainingInfoDiv.innerHTML = `
                    <i class="fas fa-exclamation-triangle"></i>
                    ${result.message}
                `;
                trainingInfoDiv.classList.add('error');
            }
        } catch (error) {
            trainingInfoDiv.innerHTML = `
                <i class="fas fa-exclamation-triangle"></i>
                Failed to load training information
            `;
            trainingInfoDiv.classList.add('error');
        }
    }

    populateForm(data) {
        Object.keys(data).forEach(key => {
            const element = document.getElementById(key);
            if (element) {
                element.value = data[key];
            }
        });
    }

    async testApiKey() {
        const testBtn = document.getElementById('testApiBtn');
        const resultSpan = document.getElementById('apiTestResult');

        testBtn.disabled = true;
        testBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Testing...';
        resultSpan.textContent = '';
        resultSpan.className = '';

        try {
            const response = await fetch('/api/status');
            const result = await response.json();

            if (result.status === 'active') {
                resultSpan.textContent = '✅ API Working';
                resultSpan.className = 'success';
                this.showToast(`API is working! Provider: ${result.provider}`, 'success');
            } else {
                resultSpan.textContent = '❌ API Failed';
                resultSpan.className = 'error';
                this.showToast(`API test failed: ${result.error || 'Unknown error'}`, 'error');
            }
        } catch (error) {
            resultSpan.textContent = '❌ Test Failed';
            resultSpan.className = 'error';
            this.showToast('Failed to test API', 'error');
        } finally {
            testBtn.disabled = false;
            testBtn.innerHTML = '<i class="fas fa-key"></i> Test API';
        }
    }
    async generateAtsKeywords() {
        console.log('Generate ATS Keywords clicked');
        const generateBtn = document.getElementById('generateAtsKeywordsBtn');
        const atsSection = document.getElementById('atsKeywordsSection');
        const atsContainer = document.getElementById('atsKeywordsContainer');

        if (!generateBtn || !atsSection || !atsContainer) {
            console.error('Required elements not found:', { generateBtn, atsSection, atsContainer });
            return;
        }

        // Check if CV is generated first
        const cvPreview = document.getElementById('cvPreview');
        if (!cvPreview || !cvPreview.innerHTML.trim()) {
            this.showToast('Please generate your CV first, then generate ATS keywords based on your complete CV', 'warning');
            return;
        }

        // Get current form data to generate contextual keywords
        const formData = this.getFormData();
        console.log('Form data for ATS keywords:', formData);

        // Extract comprehensive data from the generated CV
        const cvData = this.extractCVData();
        console.log('Extracted CV data for ATS:', cvData);

        // Check if we have enough data to generate keywords
        if (!cvData.hasContent) {
            this.showToast('Please fill in your CV information and generate CV first to create ATS keywords', 'warning');
            return;
        }

        generateBtn.disabled = true;
        generateBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Generating...';

        // Show loading in container
        atsContainer.innerHTML = '<div class="ats-loading"><i class="fas fa-spinner fa-spin"></i> Generating ATS keywords using DeepSeek...</div>';
        atsSection.style.display = 'block';

        try {
            const response = await fetch('/api/generate-ats-keywords', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(cvData)
            });

            const result = await response.json();
            console.log('ATS Keywords API Response:', result);

            if (result.success) {
                console.log('Keywords received:', result.keywords);
                this.displayAtsKeywords(result.keywords);
                this.showToast(`Generated ${result.keywords.length} ATS keywords using ${result.provider || 'DeepSeek AI'}!`, 'success');
            } else {
                throw new Error(result.error || 'Failed to generate ATS keywords');
            }
        } catch (error) {
            console.error('Error generating ATS keywords:', error);
            this.showToast('Error generating ATS keywords: ' + error.message, 'error');
            atsSection.style.display = 'none';
        } finally {
            generateBtn.disabled = false;
            generateBtn.innerHTML = '<i class="fas fa-search"></i> Generate ATS Keywords';
        }
    }

    displayAtsKeywords(keywords) {
        console.log('displayAtsKeywords called with:', keywords);
        const atsContainer = document.getElementById('atsKeywordsContainer');
        const atsSection = document.getElementById('atsKeywordsSection');

        if (!atsContainer) {
            console.error('atsKeywordsContainer not found!');
            return;
        }

        if (!keywords || keywords.length === 0) {
            console.log('No keywords to display');
            atsContainer.innerHTML = '<p class="text-muted">No keywords generated. Try filling in more information.</p>';
            return;
        }

        console.log(`Displaying ${keywords.length} keywords`);

        const keywordElements = keywords.map((keyword, index) => `
            <div class="ats-keyword" onclick="cvGenerator.toggleKeyword(this)">
                <input type="checkbox" id="keyword_${index}" style="display: none;">
                <span>${keyword.trim()}</span>
            </div>
        `).join('');

        atsContainer.innerHTML = keywordElements;

        // Make sure the section is visible
        if (atsSection) {
            atsSection.style.display = 'block';
            console.log('ATS section made visible');
        }

        console.log('Keywords displayed successfully');
    }

    toggleKeyword(element) {
        const checkbox = element.querySelector('input[type="checkbox"]');
        checkbox.checked = !checkbox.checked;
        element.classList.toggle('selected', checkbox.checked);
    }

    addSelectedKeywords() {
        const selectedKeywords = [];
        const keywordElements = document.querySelectorAll('.ats-keyword.selected');

        keywordElements.forEach(element => {
            const keywordText = element.querySelector('span').textContent;
            selectedKeywords.push(keywordText);
        });

        if (selectedKeywords.length === 0) {
            this.showToast('Please select some keywords first', 'warning');
            return;
        }

        // Add to technical skills
        const technicalSkillsInput = document.getElementById('skills_technical');
        const currentSkills = technicalSkillsInput.value.trim();

        let newSkills = currentSkills;
        selectedKeywords.forEach(keyword => {
            if (!currentSkills.toLowerCase().includes(keyword.toLowerCase())) {
                newSkills += (newSkills ? ', ' : '') + keyword;
            }
        });

        technicalSkillsInput.value = newSkills;

        // Clear selections
        keywordElements.forEach(element => {
            element.classList.remove('selected');
            element.querySelector('input[type="checkbox"]').checked = false;
        });

        this.showToast(`Added ${selectedKeywords.length} keywords to technical skills!`, 'success');
    }

    clearAtsKeywords() {
        const atsSection = document.getElementById('atsKeywordsSection');
        const atsContainer = document.getElementById('atsKeywordsContainer');

        atsContainer.innerHTML = '';
        atsSection.style.display = 'none';
    }

    extractCVData() {
        const formData = this.getFormData();
        const cvPreview = document.getElementById('cvPreview');

        // Extract all text content from the generated CV
        const cvText = cvPreview ? cvPreview.innerText : '';

        // Collect all experience titles and companies
        const experiences = [];
        const companies = [];
        const skills = [];

        // Get experience data from form
        Object.keys(formData).forEach(key => {
            if (key.includes('experience') && key.includes('title') && formData[key]) {
                experiences.push(formData[key]);
            }
            if (key.includes('experience') && key.includes('company') && formData[key]) {
                companies.push(formData[key]);
            }
        });

        // Get skills
        if (formData.skills_technical) {
            skills.push(...formData.skills_technical.split(',').map(s => s.trim()));
        }
        if (formData.skills_soft) {
            skills.push(...formData.skills_soft.split(',').map(s => s.trim()));
        }

        // Get project technologies
        Object.keys(formData).forEach(key => {
            if (key.includes('project') && key.includes('technologies') && formData[key]) {
                skills.push(...formData[key].split(',').map(s => s.trim()));
            }
        });

        return {
            name: formData.name || '',
            experiences: experiences,
            companies: companies,
            skills: [...new Set(skills)], // Remove duplicates
            education: formData.education_highest_degree || '',
            cvText: cvText,
            hasContent: experiences.length > 0 || skills.length > 0 || formData.education_highest_degree
        };
    }
    async generateCV() {
        const formData = this.getFormData();

        this.showLoading(true);

        try {
            const response = await fetch('/api/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });

            const result = await response.json();

            if (result.success) {
                this.currentCVData = result.cv_data;
                this.renderCV(result.cv_data);
                this.showToast('CV generated successfully using fine-tuned model!', 'success');
                document.getElementById('downloadPdfBtn').disabled = false;
            } else {
                throw new Error(result.error || 'Failed to generate CV');
            }
        } catch (error) {
            console.error('Error generating CV:', error);
            if (error.message.includes('DeepSeek API Error')) {
                this.showToast('DeepSeek API Error: Please check your API key and try again', 'error');
            } else {
                this.showToast('Error generating CV: ' + error.message, 'error');
            }
        } finally {
            this.showLoading(false);
        }
    }

    getFormData() {
        const form = document.getElementById('cvForm');
        const formData = new FormData(form);
        const data = {};

        for (let [key, value] of formData.entries()) {
            data[key] = value;
        }

        return data;
    }



    renderCV(data) {
        const cvPreview = document.getElementById('cvPreview');
        const template = this.getTemplate(data, this.currentTemplate);
        cvPreview.innerHTML = template;
    }

    getTemplate(data, templateType) {
        const baseTemplate = `
            <div class="cv-template ${templateType}">
                <div class="cv-header">
                    <h1 class="cv-name">${data.personal_info?.name || ''}</h1>
                    <div class="cv-contact">
                        ${data.personal_info?.email ? `<span><i class="fas fa-envelope"></i> ${data.personal_info.email}</span>` : ''}
                        ${data.personal_info?.phone ? `<span><i class="fas fa-phone"></i> ${data.personal_info.phone}</span>` : ''}
                        ${data.personal_info?.linkedin ? `<span><i class="fab fa-linkedin"></i> LinkedIn</span>` : ''}
                        ${data.personal_info?.github ? `<span><i class="fab fa-github"></i> GitHub</span>` : ''}
                    </div>
                </div>

                ${data.personal_info?.summary ? `
                <div class="cv-section">
                    <h2 class="cv-section-title"><i class="fas fa-user"></i> Professional Summary</h2>
                    <p class="cv-summary">${data.personal_info.summary}</p>
                </div>
                ` : ''}

                ${data.experience && data.experience.length > 0 ? `
                <div class="cv-section">
                    <h2 class="cv-section-title"><i class="fas fa-briefcase"></i> Work Experience</h2>
                    ${data.experience.map(exp => `
                        <div class="cv-experience-item">
                            <h3 class="cv-job-title">${exp.title || ''}</h3>
                            <div class="cv-company">${exp.company || ''}</div>
                            <div class="cv-date">${exp.start_date || ''} - ${exp.end_date || ''}</div>
                            ${exp.responsibilities && exp.responsibilities.length > 0 ? `
                                <ul class="cv-responsibilities">
                                    ${exp.responsibilities.filter(r => r).map(resp => `<li>${resp}</li>`).join('')}
                                </ul>
                            ` : ''}
                        </div>
                    `).join('')}
                </div>
                ` : ''}

                ${data.education && data.education.length > 0 ? `
                <div class="cv-section">
                    <h2 class="cv-section-title"><i class="fas fa-graduation-cap"></i> Education</h2>
                    ${data.education.map(edu => `
                        <div class="cv-education-item">
                            <h3 class="cv-degree-title">${edu.degree || ''}</h3>
                            <div class="cv-institution">${edu.institution || ''}</div>
                            <div class="cv-date">${edu.start_year || ''} - ${edu.end_year || ''}</div>
                            ${edu.gpa ? `<div class="cv-gpa">GPA: ${edu.gpa}</div>` : ''}
                        </div>
                    `).join('')}
                </div>
                ` : ''}

                ${data.skills && (data.skills.technical?.length > 0 || data.skills.soft?.length > 0) ? `
                <div class="cv-section">
                    <h2 class="cv-section-title"><i class="fas fa-cogs"></i> Skills</h2>
                    <div class="cv-skills">
                        ${data.skills.technical?.length > 0 ? `
                            <div class="cv-skill-category">
                                <h4>Technical Skills</h4>
                                <div class="cv-skill-list">
                                    ${data.skills.technical.map(skill => `<span class="cv-skill-tag">${skill}</span>`).join('')}
                                </div>
                            </div>
                        ` : ''}
                        ${data.skills.soft?.length > 0 ? `
                            <div class="cv-skill-category">
                                <h4>Soft Skills</h4>
                                <div class="cv-skill-list">
                                    ${data.skills.soft.map(skill => `<span class="cv-skill-tag">${skill}</span>`).join('')}
                                </div>
                            </div>
                        ` : ''}
                    </div>
                </div>
                ` : ''}

                ${data.projects && data.projects.length > 0 && data.projects[0].title ? `
                <div class="cv-section">
                    <h2 class="cv-section-title"><i class="fas fa-project-diagram"></i> Projects</h2>
                    ${data.projects.filter(proj => proj.title).map(proj => `
                        <div class="cv-project-item">
                            <h3 class="cv-project-title">${proj.title}</h3>
                            ${proj.description ? `<p>${proj.description}</p>` : ''}
                            ${proj.technologies?.length > 0 ? `
                                <div class="cv-skill-list">
                                    ${proj.technologies.map(tech => `<span class="cv-skill-tag">${tech}</span>`).join('')}
                                </div>
                            ` : ''}
                        </div>
                    `).join('')}
                </div>
                ` : ''}

                ${data.certifications && data.certifications.length > 0 && data.certifications[0].name ? `
                <div class="cv-section">
                    <h2 class="cv-section-title"><i class="fas fa-certificate"></i> Certifications</h2>
                    <div class="cv-certifications">
                        ${data.certifications.filter(cert => cert.name).map(cert => `
                            <div class="cv-cert-item">
                                <div class="cv-cert-name">${cert.name}</div>
                                <div class="cv-cert-issuer">${cert.issuer || ''}</div>
                                <div class="cv-cert-year">${cert.year || ''}</div>
                            </div>
                        `).join('')}
                    </div>
                </div>
                ` : ''}
            </div>
        `;

        return baseTemplate;
    }

    // Utility methods
    async handleCsvUpload(event) {
        const file = event.target.files[0];
        if (!file) return;

        const formData = new FormData();
        formData.append('file', file);

        try {
            this.showLoading(true);
            const response = await fetch('/api/upload-csv', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();

            if (result.success && result.data.length > 0) {
                // Use the first row of data
                const firstRow = result.data[0];
                this.populateForm(firstRow);
                this.showToast(`CSV uploaded successfully! Loaded ${result.count} records.`, 'success');
            } else {
                throw new Error(result.error || 'No data found in CSV');
            }
        } catch (error) {
            console.error('Error uploading CSV:', error);
            this.showToast('Error uploading CSV: ' + error.message, 'error');
        } finally {
            this.showLoading(false);
        }
    }



    downloadPDF() {
        const cvElement = document.querySelector('.cv-template');
        if (!cvElement) {
            this.showToast('No CV to download. Please generate a CV first.', 'warning');
            return;
        }

        const opt = {
            margin: 0.5,
            filename: 'cv.pdf',
            image: { type: 'jpeg', quality: 0.98 },
            html2canvas: { scale: 2 },
            jsPDF: { unit: 'in', format: 'letter', orientation: 'portrait' }
        };

        html2pdf().set(opt).from(cvElement).save();
        this.showToast('PDF download started!', 'success');
    }

    showLoading(show) {
        const overlay = document.getElementById('loadingOverlay');
        overlay.style.display = show ? 'flex' : 'none';
    }

    showToast(message, type = 'success') {
        const container = document.getElementById('toastContainer');
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;

        const icon = type === 'success' ? 'check-circle' :
                    type === 'error' ? 'exclamation-circle' :
                    'exclamation-triangle';

        toast.innerHTML = `
            <i class="fas fa-${icon} toast-icon"></i>
            <span class="toast-message">${message}</span>
        `;

        container.appendChild(toast);

        // Auto remove after 5 seconds
        setTimeout(() => {
            toast.remove();
        }, 5000);
    }

    updateLivePreview() {
        // This could be implemented to show live updates
        // For now, we'll keep it simple and only update on generate
    }
}

// Initialize the application
const cvGenerator = new CVGenerator();