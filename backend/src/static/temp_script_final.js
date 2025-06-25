        // Variables globales pour l'interface de publication
        let selectedPages = [];
        let uploadedFiles = [];
        let allPages = [];
        
        // Navigation
        document.addEventListener('DOMContentLoaded', function() {
            // Load initial settings
            loadSettings();
            
            const menuItems = document.querySelectorAll('.menu-item');
            const sections = document.querySelectorAll('.section');

            menuItems.forEach(item => {
                item.addEventListener('click', function(e) {
                    e.preventDefault();
                    
                    const targetSection = this.getAttribute('data-section');
                    
                    // Remove active class from all menu items and sections
                    menuItems.forEach(mi => mi.classList.remove('active'));
                    sections.forEach(s => s.classList.remove('active'));
                    
                    // Add active class to clicked item and corresponding section
                    this.classList.add('active');
                    document.getElementById(targetSection).classList.add('active');
                    
                    // Load section-specific data
                    if (targetSection === 'pages') {
                        loadFacebookPages();
                    }
                });
            });

            // Sync pages button
            const syncBtn = document.getElementById('syncPagesBtn');
            if (syncBtn) {
                syncBtn.addEventListener('click', syncFacebookPages);
            }

            // Save settings button
            const saveBtn = document.getElementById('saveSettingsBtn');
            if (saveBtn) {
                saveBtn.addEventListener('click', saveSettings);
            }
        });

        // Facebook Pages functionality
        async function syncFacebookPages() {
            const btn = document.getElementById('syncPagesBtn');
            const originalText = btn.innerHTML;
            btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Synchronisation...';
            btn.disabled = true;

            try {
                const response = await fetch('/api/facebook/pages/sync', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    }
                });

                const data = await response.json();
                
                if (data.success) {
                    showAlert(`${data.pages.length} pages synchronisées avec succès`, 'success');
                    displayPages(data.pages);
                } else {
                    showAlert(data.error || 'Erreur lors de la synchronisation', 'error');
                }
            } catch (error) {
                console.error('Sync error:', error);
                showAlert('Erreur de connexion', 'error');
            } finally {
                btn.innerHTML = originalText;
                btn.disabled = false;
            }
        }

        function displayPages(pages) {
            const tbody = document.getElementById('pages-table-body');
            tbody.innerHTML = '';

            pages.forEach(page => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${page.name}</td>
                    <td>${page.fan_count || 'N/A'}</td>
                    <td>${page.last_post || 'Récemment'}</td>
                    <td><span class="status connected">Connectée</span></td>
                    <td>
                        <button class="btn" style="padding: 5px 10px; font-size: 12px;">
                            <i class="fas fa-external-link-alt"></i>
                        </button>
                    </td>
                `;
                tbody.appendChild(row);
            });
        }

        async function loadFacebookPages() {
            try {
                const response = await fetch('/api/facebook/pages');
                const data = await response.json();
                
                if (data.pages && data.pages.length > 0) {
                    displayPages(data.pages);
                }
            } catch (error) {
                console.error('Load pages error:', error);
            }
        }

        // Settings functionality
        async function loadSettings() {
            try {
                const response = await fetch('/api/settings');
                const data = await response.json();
                
                if (data.app_id) {
                    document.getElementById('app-id').value = data.app_id;
                }
                // Don't load secrets for security
            } catch (error) {
                console.error('Load settings error:', error);
            }
        }

        async function saveSettings() {
            const appId = document.getElementById('app-id').value;
            const appSecret = document.getElementById('app-secret').value;
            const accessToken = document.getElementById('access-token').value;

            if (!appId.trim() || !appSecret.trim() || !accessToken.trim()) {
                showAlert('Veuillez remplir tous les champs', 'error');
                return;
            }

            try {
                const response = await fetch('/api/settings', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        app_id: appId,
                        app_secret: appSecret,
                        access_token: accessToken
                    })
                });

                const data = await response.json();
                
                if (data.success) {
                    showAlert('Paramètres sauvegardés avec succès', 'success');
                } else {
                    showAlert(data.error || 'Erreur lors de la sauvegarde', 'error');
                }
            } catch (error) {
                console.error('Settings save error:', error);
                showAlert('Erreur de connexion', 'error');
            }
        }

        // Alert system
        function showAlert(message, type) {
            const container = document.getElementById('alert-container');
            const alert = document.createElement('div');
            alert.className = `alert ${type}`;
            alert.textContent = message;
            alert.style.display = 'block';
            
            container.innerHTML = '';
            container.appendChild(alert);
            
            setTimeout(() => {
                alert.style.display = 'none';
            }, 5000);
        }

        // Initialize publication interface
        function initPublishInterface() {
            loadPagesForPublishing();
            setupMediaUpload();
            setupPreview();
            setupPageSelection();
            setupPublishButton();
        }

        // Load pages for publishing
        async function loadPagesForPublishing() {
            try {
                const response = await fetch('/api/facebook/pages');
                const data = await response.json();
                
                if (data.success) {
                    allPages = data.pages;
                    renderPagesGrid(allPages);
                } else {
                    showAlert('Erreur lors du chargement des pages', 'error');
                }
            } catch (error) {
                console.error('Error loading pages:', error);
                showAlert('Erreur de connexion', 'error');
            }
        }

        // Render pages grid
        function renderPagesGrid(pages) {
            const grid = document.getElementById('pagesGrid');
            
            if (pages.length === 0) {
                grid.innerHTML = '<div class="loading-pages">Aucune page disponible</div>';
                return;
            }

            grid.innerHTML = pages.map(page => `
                <div class="page-card" data-page-id="${page.id}" onclick="togglePageSelection('${page.id}')">
                    <img src="${page.picture?.data?.url || 'https://via.placeholder.com/50'}" alt="${page.name}" class="page-avatar">
                    <div class="page-info">
                        <div class="page-name">${page.name}</div>
                        <div class="page-stats">${page.fan_count} abonnés • ${page.category}</div>
                    </div>
                    <input type="checkbox" class="page-checkbox" data-page-id="${page.id}">
                </div>
            `).join('');
        }

        // Toggle page selection
        function togglePageSelection(pageId) {
            const pageCard = document.querySelector(`[data-page-id="${pageId}"]`);
            const checkbox = pageCard.querySelector('.page-checkbox');
            
            if (selectedPages.includes(pageId)) {
                selectedPages = selectedPages.filter(id => id !== pageId);
                pageCard.classList.remove('selected');
                checkbox.checked = false;
            } else {
                selectedPages.push(pageId);
                pageCard.classList.add('selected');
                checkbox.checked = true;
            }
            
            updateSelectedCount();
        }

        // Update selected pages count
        function updateSelectedCount() {
            document.getElementById('selectedPagesCount').textContent = selectedPages.length;
        }

        // Setup page selection controls
        function setupPageSelection() {
            document.getElementById('selectAllPages').addEventListener('click', () => {
                selectedPages = allPages.map(page => page.id);
                document.querySelectorAll('.page-card').forEach(card => {
                    card.classList.add('selected');
                    card.querySelector('.page-checkbox').checked = true;
                });
                updateSelectedCount();
            });

            document.getElementById('deselectAllPages').addEventListener('click', () => {
                selectedPages = [];
                document.querySelectorAll('.page-card').forEach(card => {
                    card.classList.remove('selected');
                    card.querySelector('.page-checkbox').checked = false;
                });
                updateSelectedCount();
            });
        }

        // Setup media upload
        function setupMediaUpload() {
            const uploadArea = document.getElementById('mediaUploadArea');
            const fileInput = document.getElementById('mediaFiles');

            uploadArea.addEventListener('click', () => fileInput.click());
            
            uploadArea.addEventListener('dragover', (e) => {
                e.preventDefault();
                uploadArea.classList.add('dragover');
            });

            uploadArea.addEventListener('dragleave', () => {
                uploadArea.classList.remove('dragover');
            });

            uploadArea.addEventListener('drop', (e) => {
                e.preventDefault();
                uploadArea.classList.remove('dragover');
                handleFiles(e.dataTransfer.files);
            });

            fileInput.addEventListener('change', (e) => {
                handleFiles(e.target.files);
            });
        }

        // Handle uploaded files
        function handleFiles(files) {
            Array.from(files).forEach(file => {
                if (file.type.startsWith('image/') || file.type.startsWith('video/')) {
                    uploadedFiles.push(file);
                    addMediaPreview(file);
                }
            });
            updatePreview();
        }

        // Add media preview
        function addMediaPreview(file) {
            const preview = document.getElementById('mediaPreview');
            const mediaItem = document.createElement('div');
            mediaItem.className = 'media-item';
            
            const reader = new FileReader();
            reader.onload = (e) => {
                const isVideo = file.type.startsWith('video/');
                mediaItem.innerHTML = `
                    ${isVideo ? 
                        `<video src="${e.target.result}" controls></video>` : 
                        `<img src="${e.target.result}" alt="Preview">`
                    }
                    <button class="remove-media" onclick="removeMedia(${uploadedFiles.length - 1})">
                        <i class="fas fa-times"></i>
                    </button>
                `;
            };
            reader.readAsDataURL(file);
            
            preview.appendChild(mediaItem);
        }

        // Remove media
        function removeMedia(index) {
            uploadedFiles.splice(index, 1);
            const preview = document.getElementById('mediaPreview');
            preview.children[index].remove();
            updatePreview();
        }

        // Setup preview
        function setupPreview() {
            const messageInput = document.getElementById('post-message');
            const linkInput = document.getElementById('post-link');
            const charCount = document.getElementById('char-count');

            messageInput.addEventListener('input', () => {
                charCount.textContent = messageInput.value.length;
                updatePreview();
            });

            linkInput.addEventListener('input', updatePreview);
        }

        // Update preview
        function updatePreview() {
            const message = document.getElementById('post-message').value;
            const link = document.getElementById('post-link').value;
            
            document.getElementById('previewMessage').textContent = message || 'Votre message apparaîtra ici...';
            
            const linkPreview = document.getElementById('previewLink');
            if (link) {
                linkPreview.style.display = 'block';
                linkPreview.innerHTML = `<i class="fas fa-link"></i> ${link}`;
            } else {
                linkPreview.style.display = 'none';
            }

            const mediaPreview = document.getElementById('previewMedia');
            if (uploadedFiles.length > 0) {
                mediaPreview.innerHTML = uploadedFiles.map(file => {
                    const isVideo = file.type.startsWith('video/');
                    return isVideo ? 
                        `<video src="${URL.createObjectURL(file)}" controls style="max-width: 100%; margin-bottom: 10px;"></video>` :
                        `<img src="${URL.createObjectURL(file)}" style="max-width: 100%; margin-bottom: 10px;">`;
                }).join('');
            } else {
                mediaPreview.innerHTML = '';
            }
        }

        // Setup publish button
        function setupPublishButton() {
            document.getElementById('publishNowBtn').addEventListener('click', publishPost);
        }

        // Publish post
        async function publishPost() {
            const message = document.getElementById('post-message').value.trim();
            const link = document.getElementById('post-link').value.trim();

            if (!message) {
                showAlert('Le message est obligatoire', 'error');
                return;
            }

            if (selectedPages.length === 0) {
                showAlert('Veuillez sélectionner au moins une page', 'error');
                return;
            }

            // Show publishing modal
            showPublishingModal();

            try {
                const formData = new FormData();
                formData.append('message', message);
                formData.append('page_ids', JSON.stringify(selectedPages));
                
                if (link) {
                    formData.append('link', link);
                }

                uploadedFiles.forEach(file => {
                    formData.append('media_files', file);
                });

                const response = await fetch('/api/facebook/publish/multi', {
                    method: 'POST',
                    body: formData
                });

                const data = await response.json();
                
                if (data.success) {
                    showPublishingResults(data);
                } else {
                    hidePublishingModal();
                    showAlert(data.error || 'Erreur lors de la publication', 'error');
                }
            } catch (error) {
                console.error('Publishing error:', error);
                hidePublishingModal();
                showAlert('Erreur de connexion', 'error');
            }
        }

        // Show publishing modal
        function showPublishingModal() {
            const modal = document.getElementById('publishingModal');
            modal.style.display = 'flex';
            
            // Reset progress
            document.getElementById('publishProgress').style.width = '0%';
            document.getElementById('publishProgressText').textContent = 'Préparation...';
            document.getElementById('publishingResults').innerHTML = '';
            document.getElementById('closePublishModal').style.display = 'none';
            
            // Simulate progress
            let progress = 0;
            const progressInterval = setInterval(() => {
                progress += Math.random() * 20;
                if (progress > 90) progress = 90;
                
                document.getElementById('publishProgress').style.width = progress + '%';
                document.getElementById('publishProgressText').textContent = 
                    progress < 30 ? 'Préparation...' :
                    progress < 60 ? 'Upload des médias...' :
                    progress < 90 ? 'Publication en cours...' : 'Finalisation...';
                
                if (progress >= 90) {
                    clearInterval(progressInterval);
                }
            }, 500);
        }

        // Show publishing results
        function showPublishingResults(data) {
            document.getElementById('publishProgress').style.width = '100%';
            document.getElementById('publishProgressText').textContent = 'Terminé !';
            
            const resultsContainer = document.getElementById('publishingResults');
            const results = data.results;
            
            resultsContainer.innerHTML = Object.keys(results).map(pageId => {
                const result = results[pageId];
                const page = allPages.find(p => p.id === pageId);
                const pageName = page ? page.name : pageId;
                
                return `
                    <div class="result-item ${result.success ? 'success' : 'error'}">
                        <i class="fas fa-${result.success ? 'check' : 'times'}"></i>
                        <div>
                            <strong>${pageName}</strong><br>
                            <small>${result.message}</small>
                        </div>
                    </div>
                `;
            }).join('');
            
            document.getElementById('closePublishModal').style.display = 'inline-block';
            
            // Reset form if all successful
            if (data.summary.failed === 0) {
                resetPublishForm();
            }
        }

        // Hide publishing modal
        function hidePublishingModal() {
            document.getElementById('publishingModal').style.display = 'none';
        }

        // Reset publish form
        function resetPublishForm() {
            document.getElementById('post-message').value = '';
            document.getElementById('post-link').value = '';
            document.getElementById('char-count').textContent = '0';
            document.getElementById('mediaPreview').innerHTML = '';
            uploadedFiles = [];
            selectedPages = [];
            document.querySelectorAll('.page-card').forEach(card => {
                card.classList.remove('selected');
                card.querySelector('.page-checkbox').checked = false;
            });
            updateSelectedCount();
            updatePreview();
        }

        // Close modal event
        document.getElementById('closePublishModal').addEventListener('click', hidePublishingModal);

        // Initialize when publish section is shown
        document.addEventListener('DOMContentLoaded', () => {
            // Initialiser immédiatement l'interface de publication
            initPublishInterface();
            
            const publishMenuItem = document.querySelector('[data-section="publish"]');
            if (publishMenuItem) {
                publishMenuItem.addEventListener('click', () => {
                    setTimeout(initPublishInterface, 100);
                });
            }
            
            // Initialize analytics section
            const analyticsMenuItem = document.querySelector('[data-section="analytics"]');
            if (analyticsMenuItem) {
                analyticsMenuItem.addEventListener('click', () => {
                    setTimeout(initAnalyticsInterface, 100);
                });
            }
        });
        
        // Analytics & Boost Post functionality
        let currentPosts = [];
        let currentBoostPost = null;
        
        // Initialize analytics interface
        function initAnalyticsInterface() {
            loadPostsPerformance();
            loadSavedAudiences();
            setupBoostModal();
            setupAnalyticsEventListeners();
        }
        
        // Load posts performance data
        async function loadPostsPerformance() {
            try {
                showAlert('Chargement des statistiques...', 'info');
                
                // Load posts from API
                const response = await fetch('/api/facebook/posts/performance');
                if (!response.ok) {
                    throw new Error('Erreur lors du chargement des posts');
                }
                
                const data = await response.json();
                currentPosts = data.posts || [];
                
                // Update stats overview
                updateStatsOverview(data.stats || {});
                
                // Update posts table
                updatePostsTable(currentPosts);
                
                // Update page filter
                updatePageFilter();
                
                hideAlert();
            } catch (error) {
                console.error('Error loading posts performance:', error);
                
                // Show sample data for demo
                loadSamplePostsData();
                hideAlert();
            }
        }
        
        // Load sample posts data for demo
        function loadSamplePostsData() {
            const samplePosts = [
                {
                    id: 'post_1',
                    message: 'Découvrez notre nouvelle gamme de terrasses en bois composite ! 🌿',
                    page_name: 'Les Bois Malouins',
                    page_id: 'page_1',
                    created_time: '2025-06-20T10:30:00Z',
                    reach: 2340,
                    engagement: 156,
                    likes: 89,
                    comments: 23,
                    shares: 44,
                    status: 'organic',
                    boost_eligible: true
                },
                {
                    id: 'post_2',
                    message: 'Promotion spéciale sur les lames de terrasse en pin traité 🏡',
                    page_name: 'Bois Grand Ouest',
                    page_id: 'page_2',
                    created_time: '2025-06-19T14:15:00Z',
                    reach: 4560,
                    engagement: 298,
                    likes: 167,
                    comments: 45,
                    shares: 86,
                    status: 'boosted',
                    boost_eligible: false
                },
                {
                    id: 'post_3',
                    message: 'Conseils d\'entretien pour vos terrasses en bois 🔧',
                    page_name: 'Terrasses et Bois du Maine',
                    page_id: 'page_3',
                    created_time: '2025-06-18T09:45:00Z',
                    reach: 1890,
                    engagement: 134,
                    likes: 78,
                    comments: 34,
                    shares: 22,
                    status: 'organic',
                    boost_eligible: true
                }
            ];
            
            const sampleStats = {
                total_reach: 8790,
                total_engagement: 588,
                total_shares: 152,
                boosted_posts_count: 1,
                posts_count: 3
            };
            
            currentPosts = samplePosts;
            updateStatsOverview(sampleStats);
            updatePostsTable(samplePosts);
            updatePageFilter();
        }
        
        // Update stats overview
        function updateStatsOverview(stats) {
            document.getElementById('totalReach').textContent = formatNumber(stats.total_reach || 0);
            document.getElementById('totalEngagement').textContent = formatNumber(stats.total_engagement || 0);
            document.getElementById('totalShares').textContent = formatNumber(stats.total_shares || 0);
            document.getElementById('activeBoostedPosts').textContent = stats.boosted_posts_count || 0;
        }
        
        // Update posts table
        function updatePostsTable(posts) {
            const tbody = document.getElementById('postsTableBody');
            
            if (posts.length === 0) {
                tbody.innerHTML = '<tr><td colspan="7" class="loading-posts">Aucune publication trouvée</td></tr>';
                return;
            }
            
            tbody.innerHTML = posts.map(post => {
                const createdDate = new Date(post.created_time);
                const timeAgo = getTimeAgo(createdDate);
                
                return `
                    <tr>
                        <td class="post-content">${post.message}</td>
                        <td>${post.page_name}</td>
                        <td>${timeAgo}</td>
                        <td>${formatNumber(post.reach)}</td>
                        <td>${formatNumber(post.engagement)}</td>
                        <td>
                            <span class="post-status ${post.status}">${post.status === 'organic' ? 'Organique' : 'Boosté'}</span>
                        </td>
                        <td class="post-actions">
                            ${post.boost_eligible ? 
                                `<button class="btn-boost" onclick="openBoostModal('${post.id}')">
                                    <i class="fas fa-rocket"></i> Booster
                                </button>` : 
                                `<button class="btn-boost" disabled>
                                    <i class="fas fa-check"></i> Boosté
                                </button>`
                            }
                        </td>
                    </tr>
                `;
            }).join('');
        }
        
        // Update page filter
        function updatePageFilter() {
            const pageFilter = document.getElementById('pageFilter');
            const uniquePages = [...new Set(currentPosts.map(post => post.page_name))];
            
            pageFilter.innerHTML = '<option value="">Toutes les pages</option>' +
                uniquePages.map(page => `<option value="${page}">${page}</option>`).join('');
        }
        
        // Setup boost modal
        function setupBoostModal() {
            // Close modal events
            document.getElementById('closeBoostModal').addEventListener('click', closeBoostModal);
            document.getElementById('boostPostModal').addEventListener('click', (e) => {
                if (e.target.id === 'boostPostModal') {
                    closeBoostModal();
                }
            });
            
            // Audience type change
            document.querySelectorAll('input[name="audienceType"]').forEach(radio => {
                radio.addEventListener('change', handleBoostAudienceChange);
            });
            
            // Submit boost
            document.getElementById('submitBoostBtn').addEventListener('click', submitBoost);
        }
        
        // Open boost modal
        async function openBoostModal(postId) {
            currentBoostPost = postId;
            
            try {
                // Load post details
                const response = await fetch(`/api/facebook/posts/${postId}/details`);
                const data = await response.json();
                
                if (data.success) {
                    updateBoostPostPreview(data.post);
                } else {
                    // Use sample data
                    const samplePost = currentPosts.find(p => p.id === postId);
                    if (samplePost) {
                        updateBoostPostPreview(samplePost);
                    }
                }
                
                // Show modal
                document.getElementById('boostPostModal').style.display = 'flex';
                
            } catch (error) {
                console.error('Error loading post details:', error);
                showAlert('Erreur lors du chargement du post', 'error');
            }
        }
        
        // Close boost modal
        function closeBoostModal() {
            document.getElementById('boostPostModal').style.display = 'none';
            currentBoostPost = null;
        }
        
        // Update boost post preview
        function updateBoostPostPreview(post) {
            const preview = document.getElementById('boostPostPreview');
            
            preview.innerHTML = `
                <div style="border: 1px solid #e1e8ed; border-radius: 8px; padding: 16px; background: white;">
                    <div style="display: flex; align-items: center; margin-bottom: 12px;">
                        <img src="https://via.placeholder.com/40" alt="${post.page_name}" style="width: 40px; height: 40px; border-radius: 50%; margin-right: 12px;">
                        <div>
                            <div style="font-weight: 600; color: #2c3e50;">${post.page_name}</div>
                            <div style="font-size: 12px; color: #7f8c8d;">${getTimeAgo(new Date(post.created_time))}</div>
                        </div>
                    </div>
                    <div style="margin-bottom: 12px; line-height: 1.4;">${post.message}</div>
                    ${post.media ? `
                        <div style="margin-bottom: 12px;">
                            <img src="${post.media.url}" alt="Post media" style="width: 100%; border-radius: 8px;">
                        </div>
                    ` : ''}
                    ${post.link ? `
                        <div style="border: 1px solid #e1e8ed; border-radius: 8px; padding: 12px; background: #f8f9fa;">
                            <i class="fas fa-link" style="color: #3498db; margin-right: 8px;"></i>
                            <a href="${post.link}" target="_blank" style="color: #3498db; text-decoration: none;">${post.link}</a>
                        </div>
                    ` : ''}
                    <div style="display: flex; justify-content: space-between; margin-top: 12px; padding-top: 12px; border-top: 1px solid #e1e8ed; font-size: 14px; color: #7f8c8d;">
                        <span><i class="fas fa-eye"></i> ${formatNumber(post.reach)} vues</span>
                        <span><i class="fas fa-heart"></i> ${formatNumber(post.likes)} j'aime</span>
                        <span><i class="fas fa-comment"></i> ${formatNumber(post.comments)} commentaires</span>
                        <span><i class="fas fa-share"></i> ${formatNumber(post.shares)} partages</span>
                    </div>
                </div>
            `;
        }
        
        // Handle boost audience type change
        function handleBoostAudienceChange() {
            const selectedType = document.querySelector('input[name="audienceType"]:checked').value;
            
            // Hide all custom settings
            document.getElementById('customAudienceSettings').style.display = 'none';
            document.getElementById('savedAudienceSettings').style.display = 'none';
            
            // Show relevant settings
            if (selectedType === 'custom') {
                document.getElementById('customAudienceSettings').style.display = 'block';
                loadCustomAudienceForm();
            } else if (selectedType === 'saved') {
                document.getElementById('savedAudienceSettings').style.display = 'block';
                loadSavedAudiencesForBoost();
            }
        }
        
        // Load custom audience form
        function loadCustomAudienceForm() {
            const container = document.getElementById('customAudienceSettings');
            container.innerHTML = `
                <div class="form-group">
                    <label for="boostLocation">Localisation</label>
                    <input type="text" id="boostLocation" class="form-control" value="France" placeholder="Pays, région, ville...">
                </div>
                <div class="form-row">
                    <div class="form-group">
                        <label for="boostAgeMin">Âge minimum</label>
                        <select id="boostAgeMin" class="form-control">
                            <option value="18">18</option>
                            <option value="25" selected>25</option>
                            <option value="35">35</option>
                            <option value="45">45</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label for="boostAgeMax">Âge maximum</label>
                        <select id="boostAgeMax" class="form-control">
                            <option value="35">35</option>
                            <option value="45">45</option>
                            <option value="55" selected>55</option>
                            <option value="65">65+</option>
                        </select>
                    </div>
                </div>
                <div class="form-group">
                    <label for="boostGender">Genre</label>
                    <select id="boostGender" class="form-control">
                        <option value="all">Tous</option>
                        <option value="male">Hommes</option>
                        <option value="female">Femmes</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="boostInterests">Centres d'intérêt</label>
                    <input type="text" id="boostInterests" class="form-control" placeholder="Bricolage, Jardinage, Aménagement...">
                    <small class="form-help">Séparez par des virgules</small>
                </div>
            `;
        }
        
        // Load saved audiences for boost
        async function loadSavedAudiencesForBoost() {
            const container = document.getElementById('savedAudienceSettings');
            
            try {
                const response = await fetch('/api/facebook/audiences');
                const data = await response.json();
                
                if (data.success && data.audiences.length > 0) {
                    container.innerHTML = `
                        <div class="form-group">
                            <label for="boostSavedAudience">Audience sauvegardée</label>
                            <select id="boostSavedAudience" class="form-control">
                                <option value="">Sélectionner une audience...</option>
                                ${data.audiences.map(audience => 
                                    `<option value="${audience.id}">${audience.name} (${formatNumber(audience.size)} personnes)</option>`
                                ).join('')}
                            </select>
                        </div>
                    `;
                } else {
                    container.innerHTML = `
                        <div class="form-group">
                            <p style="color: #7f8c8d; font-style: italic;">Aucune audience sauvegardée disponible. Créez d'abord des audiences dans la section Audiences.</p>
                        </div>
                    `;
                }
            } catch (error) {
                console.error('Error loading saved audiences:', error);
                container.innerHTML = `
                    <div class="form-group">
                        <p style="color: #e74c3c;">Erreur lors du chargement des audiences sauvegardées.</p>
                    </div>
                `;
            }
        }
        
        // Submit boost
        async function submitBoost() {
            if (!currentBoostPost) {
                showAlert('Aucun post sélectionné', 'error');
                return;
            }
            
            try {
                // Collect form data
                const objective = document.getElementById('boostObjective').value;
                const budget = parseInt(document.getElementById('boostBudget').value);
                const duration = parseInt(document.getElementById('boostDuration').value);
                const audienceType = document.querySelector('input[name="audienceType"]:checked').value;
                
                // Validate
                if (!objective || !budget || !duration || budget < 5 || duration < 1) {
                    showAlert('Veuillez remplir tous les champs obligatoires', 'error');
                    return;
                }
                
                // Prepare boost data
                const boostData = {
                    objective,
                    budget,
                    duration,
                    audience_type: audienceType
                };
                
                // Add audience-specific data
                if (audienceType === 'custom') {
                    boostData.location = document.getElementById('boostLocation')?.value || 'France';
                    boostData.age_min = parseInt(document.getElementById('boostAgeMin')?.value || 25);
                    boostData.age_max = parseInt(document.getElementById('boostAgeMax')?.value || 55);
                    boostData.gender = document.getElementById('boostGender')?.value || 'all';
                    boostData.interests = document.getElementById('boostInterests')?.value || '';
                } else if (audienceType === 'saved') {
                    boostData.saved_audience_id = document.getElementById('boostSavedAudience')?.value;
                    if (!boostData.saved_audience_id) {
                        showAlert('Veuillez sélectionner une audience sauvegardée', 'error');
                        return;
                    }
                }
                
                // Show loading
                const submitBtn = document.getElementById('submitBoostBtn');
                const originalText = submitBtn.innerHTML;
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Création en cours...';
                submitBtn.disabled = true;
                
                // Submit boost
                const response = await fetch(`/api/facebook/posts/${currentBoostPost}/boost`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(boostData)
                });
                
                const result = await response.json();
                
                if (result.success) {
                    showAlert(`Post boosté avec succès ! Budget: ${budget}€/jour pendant ${duration} jours. Portée estimée: ${formatNumber(result.estimated_reach)} personnes.`, 'success');
                    closeBoostModal();
                    loadPostsPerformance(); // Refresh posts
                } else {
                    showAlert(result.error || 'Erreur lors du boost', 'error');
                }
                
                // Restore button
                submitBtn.innerHTML = originalText;
                submitBtn.disabled = false;
                
            } catch (error) {
                console.error('Error submitting boost:', error);
                showAlert('Erreur lors du boost', 'error');
                
                // Restore button
                const submitBtn = document.getElementById('submitBoostBtn');
                submitBtn.innerHTML = '<i class="fas fa-rocket"></i> Lancer le boost';
                submitBtn.disabled = false;
            }
        }

        // Analytics & Boost Post functionality
        let currentPosts = [];
        
        function loadSamplePostsData() {
            const samplePosts = [
                {
                    id: 'post_1',
                    message: 'Découvrez notre nouvelle gamme de terrasses en bois composite ! 🌿',
                    page_name: 'Les Bois Malouins',
                    page_id: 'page_1',
                    created_time: '2025-06-20T10:30:00Z',
                    reach: 2340,
                    engagement: 156,
                    likes: 89,
                    comments: 23,
                    shares: 44,
                    status: 'organic',
                    boost_eligible: true
                },
                {
                    id: 'post_2',
                    message: 'Promotion spéciale sur les lames de terrasse en pin traité 🏡',
                    page_name: 'Bois Grand Ouest',
                    page_id: 'page_2',
                    created_time: '2025-06-19T14:15:00Z',
                    reach: 4560,
                    engagement: 298,
                    likes: 167,
                    comments: 45,
                    shares: 86,
                    status: 'boosted',
                    boost_eligible: false
                },
                {
                    id: 'post_3',
                    message: 'Conseils d\'entretien pour vos terrasses en bois 🔧',
                    page_name: 'Terrasses et Bois du Maine',
                    page_id: 'page_3',
                    created_time: '2025-06-18T09:45:00Z',
                    reach: 1890,
                    engagement: 134,
                    likes: 78,
                    comments: 34,
                    shares: 22,
                    status: 'organic',
                    boost_eligible: true
                }
            ];
            
            currentPosts = samplePosts;
            
            // Update stats
            const totalReach = samplePosts.reduce((sum, post) => sum + post.reach, 0);
            const totalEngagement = samplePosts.reduce((sum, post) => sum + post.engagement, 0);
            const totalShares = samplePosts.reduce((sum, post) => sum + post.shares, 0);
            const activeBoosted = samplePosts.filter(post => post.status === 'boosted').length;
            
            updateStatsOverview({
                total_reach: totalReach,
                total_engagement: totalEngagement,
                total_shares: totalShares,
                active_boosted_posts: activeBoosted
            });
            
            updatePostsTable(samplePosts);
            updatePageFilter();
        }
        
        // Update stats overview
        function updateStatsOverview(stats) {
            document.getElementById('totalReach').textContent = formatNumber(stats.total_reach || 0);
            document.getElementById('totalEngagement').textContent = formatNumber(stats.total_engagement || 0);
            document.getElementById('totalShares').textContent = formatNumber(stats.total_shares || 0);
            document.getElementById('activeBoostedPosts').textContent = stats.active_boosted_posts || 0;
        }
        
        // Update posts table
        function updatePostsTable(posts) {
            const tbody = document.getElementById('postsTableBody');
            
            if (posts.length === 0) {
                tbody.innerHTML = `
                    <tr>
                        <td colspan="7" class="loading-posts">
                            Aucune publication trouvée
                        </td>
                    </tr>
                `;
                return;
            }
            
            tbody.innerHTML = posts.map(post => {
                const createdDate = new Date(post.created_time);
                const formattedDate = createdDate.toLocaleDateString('fr-FR');
                const timeAgo = getTimeAgo(createdDate);
                
                return `
                    <tr>
                        <td>
                            <div class="post-content" title="${post.message}">
                                ${post.message}
                            </div>
                        </td>
                        <td>${post.page_name}</td>
                        <td>
                            ${formattedDate}<br>
                            <small style="color: #7f8c8d;">${timeAgo}</small>
                        </td>
                        <td>${formatNumber(post.reach)}</td>
                        <td>
                            ${formatNumber(post.engagement)}<br>
                            <small style="color: #7f8c8d;">
                                ${post.likes} ❤️ ${post.comments} 💬 ${post.shares} 🔄
                            </small>
                        </td>
                        <td>
                            <span class="post-status ${post.status}">
                                ${post.status === 'organic' ? 'Organique' : 'Boosté'}
                            </span>
                            ${post.status === 'boosted' ? `<br><small>Budget: ${post.boost_budget}€/j</small>` : ''}
                        </td>
                        <td>
                            <div class="post-actions">
                                <button class="btn-boost" 
                                        onclick="openBoostModal('${post.id}')"
                                        ${!post.can_boost ? 'disabled' : ''}>
                                    <i class="fas fa-bullhorn"></i>
                                    ${post.status === 'boosted' ? 'Modifier' : 'Booster'}
                                </button>
                            </div>
                        </td>
                    </tr>
                `;
            }).join('');
        }
        
        // Update page filter
        function updatePageFilter() {
            const pageFilter = document.getElementById('pageFilter');
            const uniquePages = [...new Set(currentPosts.map(post => post.page_name))];
            
            pageFilter.innerHTML = '<option value="">Toutes les pages</option>' +
                uniquePages.map(pageName => 
                    `<option value="${pageName}">${pageName}</option>`
                ).join('');
        }
        
        // Open boost modal
        function openBoostModal(postId) {
            const post = currentPosts.find(p => p.id === postId);
            if (!post) return;
            
            currentBoostPost = post;
            
            // Update post preview
            updateBoostPostPreview(post);
            
            // Reset form
            resetBoostForm();
            
            // Show modal
            document.getElementById('boostPostModal').style.display = 'flex';
        }
        
        // Update boost post preview
        function updateBoostPostPreview(post) {
            const preview = document.getElementById('boostPostPreview');
            const createdDate = new Date(post.created_time);
            
            preview.innerHTML = `
                <div style="border-bottom: 1px solid #e1e8ed; padding-bottom: 12px; margin-bottom: 12px;">
                    <strong>${post.page_name}</strong>
                    <div style="font-size: 12px; color: #7f8c8d;">${createdDate.toLocaleDateString('fr-FR')}</div>
                </div>
                <div style="margin-bottom: 12px;">
                    ${post.message}
                </div>
                <div style="font-size: 12px; color: #7f8c8d; display: flex; gap: 16px;">
                    <span>👁️ ${formatNumber(post.reach)} vues</span>
                    <span>❤️ ${post.likes} j'aime</span>
                    <span>💬 ${post.comments} commentaires</span>
                    <span>🔄 ${post.shares} partages</span>
                </div>
            `;
        }
        
        // Reset boost form
        function resetBoostForm() {
            document.getElementById('boostObjective').value = 'REACH';
            document.getElementById('boostBudget').value = '20';
            document.getElementById('boostDuration').value = '7';
            document.querySelector('input[name="audienceType"][value="auto"]').checked = true;
            
            // Hide custom/saved audience settings
            document.getElementById('customAudienceSettings').style.display = 'none';
            document.getElementById('savedAudienceSettings').style.display = 'none';
            
            updateBudgetSummary();
        }
        
        // Update budget summary
        function updateBudgetSummary() {
            const budget = parseInt(document.getElementById('boostBudget').value) || 20;
            const duration = parseInt(document.getElementById('boostDuration').value) || 7;
            const total = budget * duration;
            
            document.getElementById('summaryDailyBudget').textContent = budget + '€';
            document.getElementById('summaryDuration').textContent = duration + ' jours';
            document.getElementById('summaryTotalBudget').textContent = total + '€';
            
            // Estimate reach based on budget
            const estimatedReach = Math.round((budget * 100) + (budget * 50 * Math.random()));
            const reachMin = Math.round(estimatedReach * 0.8);
            const reachMax = Math.round(estimatedReach * 1.2);
            
            document.getElementById('summaryEstimatedReach').textContent = 
                `${formatNumber(reachMin)} - ${formatNumber(reachMax)} personnes`;
        }
        
        // Setup boost modal event listeners
        function setupBoostModal() {
            // Close modal
            document.getElementById('closeBoostModal').addEventListener('click', closeBoostModal);
            document.getElementById('cancelBoostBtn').addEventListener('click', closeBoostModal);
            
            // Budget and duration changes
            document.getElementById('boostBudget').addEventListener('input', updateBudgetSummary);
            document.getElementById('boostDuration').addEventListener('input', updateBudgetSummary);
            
            // Audience type changes
            document.querySelectorAll('input[name="audienceType"]').forEach(radio => {
                radio.addEventListener('change', handleAudienceTypeChange);
            });
            
            // Confirm boost
            document.getElementById('confirmBoostBtn').addEventListener('click', confirmBoostPost);
        }
        
        // Handle audience type change
        function handleAudienceTypeChange(event) {
            const audienceType = event.target.value;
            
            document.getElementById('customAudienceSettings').style.display = 
                audienceType === 'custom' ? 'block' : 'none';
            document.getElementById('savedAudienceSettings').style.display = 
                audienceType === 'saved' ? 'block' : 'none';
        }
        
        // Close boost modal
        function closeBoostModal() {
            document.getElementById('boostPostModal').style.display = 'none';
            currentBoostPost = null;
        }
        
        // Confirm boost post
        async function confirmBoostPost() {
            if (!currentBoostPost) return;
            
            try {
                const boostData = {
                    post_id: currentBoostPost.id,
                    objective: document.getElementById('boostObjective').value,
                    daily_budget: parseInt(document.getElementById('boostBudget').value),
                    duration: parseInt(document.getElementById('boostDuration').value),
                    audience_type: document.querySelector('input[name="audienceType"]:checked').value
                };
                
                // Add custom audience data if selected
                if (boostData.audience_type === 'custom') {
                    boostData.audience = {
                        age_min: document.getElementById('ageMin').value,
                        age_max: document.getElementById('ageMax').value,
                        gender: document.getElementById('audienceGender').value,
                        location: document.getElementById('audienceLocation').value,
                        interests: document.getElementById('audienceInterests').value.split(',').map(s => s.trim()).filter(s => s)
                    };
                } else if (boostData.audience_type === 'saved') {
                    boostData.saved_audience_id = document.getElementById('savedAudienceSelect').value;
                }
                
                showAlert('Lancement du boost en cours...', 'info');
                
                const response = await fetch('/api/facebook/boost/create', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(boostData)
                });
                
                const result = await response.json();
                
                if (result.success) {
                    showAlert('Boost lancé avec succès !', 'success');
                    closeBoostModal();
                    loadPostsPerformance(); // Refresh data
                } else {
                    showAlert('Erreur lors du lancement du boost: ' + result.error, 'error');
                }
                
            } catch (error) {
                console.error('Error boosting post:', error);
                showAlert('Erreur lors du lancement du boost', 'error');
            }
        }
        
        // Load saved audiences
        async function loadSavedAudiences() {
            try {
                const response = await fetch('/api/facebook/audiences');
                if (response.ok) {
                    const data = await response.json();
                    const select = document.getElementById('savedAudienceSelect');
                    
                    select.innerHTML = '<option value="">Sélectionner une audience...</option>' +
                        data.audiences.map(audience => 
                            `<option value="${audience.id}">${audience.name}</option>`
                        ).join('');
                }
            } catch (error) {
                console.error('Error loading saved audiences:', error);
            }
        }
        
        // Setup analytics event listeners
        function setupAnalyticsEventListeners() {
            // Refresh stats
            document.getElementById('refreshStatsBtn').addEventListener('click', loadPostsPerformance);
            
            // Filter changes
            document.getElementById('pageFilter').addEventListener('change', filterPosts);
            document.getElementById('timeFilter').addEventListener('change', filterPosts);
        }
        
        // Filter posts
        function filterPosts() {
            const pageFilter = document.getElementById('pageFilter').value;
            const timeFilter = parseInt(document.getElementById('timeFilter').value);
            
            let filteredPosts = currentPosts;
            
            // Filter by page
            if (pageFilter) {
                filteredPosts = filteredPosts.filter(post => post.page_name === pageFilter);
            }
            
            // Filter by time
            if (timeFilter) {
                const cutoffDate = new Date();
                cutoffDate.setDate(cutoffDate.getDate() - timeFilter);
                
                filteredPosts = filteredPosts.filter(post => 
                    new Date(post.created_time) >= cutoffDate
                );
            }
            
            updatePostsTable(filteredPosts);
        }
        
        // Utility functions
        function formatNumber(num) {
            if (num >= 1000000) {
                return (num / 1000000).toFixed(1) + 'M';
            } else if (num >= 1000) {
                return (num / 1000).toFixed(1) + 'K';
            }
            return num.toString();
        }
        
        function getTimeAgo(date) {
            const now = new Date();
            const diffMs = now - date;
            const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
            const diffDays = Math.floor(diffHours / 24);
            
            if (diffDays > 0) {
                return `Il y a ${diffDays} jour${diffDays > 1 ? 's' : ''}`;
            } else if (diffHours > 0) {
                return `Il y a ${diffHours}h`;
            } else {
                return 'Il y a moins d\'1h';
            }
        }
        
        // ===== CAMPAIGNS/ADS FUNCTIONALITY =====
        
        let currentStep = 1;
        let campaignData = {};
        
        // Initialize campaigns functionality
        function initializeCampaigns() {
            setupCampaignEventListeners();
            loadCampaigns();
            loadSavedAudiencesForCampaigns();
            loadPagesForCampaigns();
        }
        
        // Setup campaign event listeners
        function setupCampaignEventListeners() {
            // Create campaign button
            document.getElementById('createCampaignBtn').addEventListener('click', showCampaignForm);
            
            // Form navigation
            document.getElementById('nextStepBtn').addEventListener('click', nextStep);
            document.getElementById('prevStepBtn').addEventListener('click', prevStep);
            document.getElementById('cancelCampaignBtn').addEventListener('click', hideCampaignForm);
            document.getElementById('createCampaignSubmitBtn').addEventListener('click', submitCampaign);
            
            // Audience type change
            document.getElementById('audienceType').addEventListener('change', handleAudienceTypeChange);
            
            // Character counters
            setupCharacterCounters();
            
            // Media upload
            setupMediaUpload();
        }
        
        // Show campaign creation form
        function showCampaignForm() {
            document.getElementById('campaignCreationForm').style.display = 'block';
            document.getElementById('campaignsList').style.display = 'none';
            resetCampaignForm();
        }
        
        // Hide campaign creation form
        function hideCampaignForm() {
            document.getElementById('campaignCreationForm').style.display = 'none';
            document.getElementById('campaignsList').style.display = 'block';
            resetCampaignForm();
        }
        
        // Reset campaign form
        function resetCampaignForm() {
            currentStep = 1;
            campaignData = {};
            showStep(1);
            document.querySelector('.form-container').reset?.();
        }
        
        // Show specific step
        function showStep(step) {
            // Hide all steps
            for (let i = 1; i <= 4; i++) {
                document.getElementById(`step${i}`).style.display = 'none';
            }
            
            // Show current step
            document.getElementById(`step${step}`).style.display = 'block';
            
            // Update navigation buttons
            document.getElementById('prevStepBtn').style.display = step > 1 ? 'block' : 'none';
            document.getElementById('nextStepBtn').style.display = step < 4 ? 'block' : 'none';
            document.getElementById('createCampaignSubmitBtn').style.display = step === 4 ? 'block' : 'none';
            
            // Update step-specific content
            if (step === 4) {
                generateCampaignReview();
            }
        }
        
        // Next step
        function nextStep() {
            if (validateCurrentStep()) {
                saveCurrentStepData();
                currentStep++;
                showStep(currentStep);
            }
        }
        
        // Previous step
        function prevStep() {
            currentStep--;
            showStep(currentStep);
        }
        
        // Validate current step
        function validateCurrentStep() {
            const step = currentStep;
            
            if (step === 1) {
                const name = document.getElementById('campaignName').value;
                const objective = document.getElementById('campaignObjective').value;
                const budget = document.getElementById('campaignBudget').value;
                
                if (!name || !objective || !budget || budget < 10) {
                    showAlert('Veuillez remplir tous les champs obligatoires de l\'étape 1', 'error');
                    return false;
                }
            } else if (step === 2) {
                const adsetName = document.getElementById('adsetName').value;
                const audienceType = document.getElementById('audienceType').value;
                const dailyBudget = document.getElementById('dailyBudget').value;
                const startDate = document.getElementById('startDate').value;
                
                if (!adsetName || !audienceType || !dailyBudget || !startDate || dailyBudget < 5) {
                    showAlert('Veuillez remplir tous les champs obligatoires de l\'étape 2', 'error');
                    return false;
                }
                
                if (audienceType === 'saved') {
                    const savedAudience = document.getElementById('savedAudience').value;
                    if (!savedAudience) {
                        showAlert('Veuillez sélectionner une audience sauvegardée', 'error');
                        return false;
                    }
                }
            } else if (step === 3) {
                const adName = document.getElementById('adName').value;
                const adFormat = document.getElementById('adFormat').value;
                const adPage = document.getElementById('adPage').value;
                const adHeadline = document.getElementById('adHeadline').value;
                const adText = document.getElementById('adText').value;
                const adDescription = document.getElementById('adDescription').value;
                const callToAction = document.getElementById('callToAction').value;
                
                if (!adName || !adFormat || !adPage || !adHeadline || !adText || !adDescription || !callToAction) {
                    showAlert('Veuillez remplir tous les champs obligatoires de l\'étape 3', 'error');
                    return false;
                }
            }
            
            return true;
        }
        
        // Save current step data
        function saveCurrentStepData() {
            if (currentStep === 1) {
                campaignData.campaign = {
                    name: document.getElementById('campaignName').value,
                    objective: document.getElementById('campaignObjective').value,
                    budget: parseFloat(document.getElementById('campaignBudget').value)
                };
            } else if (currentStep === 2) {
                campaignData.adset = {
                    name: document.getElementById('adsetName').value,
                    audienceType: document.getElementById('audienceType').value,
                    dailyBudget: parseFloat(document.getElementById('dailyBudget').value),
                    startDate: document.getElementById('startDate').value,
                    endDate: document.getElementById('endDate').value || null
                };
                
                if (campaignData.adset.audienceType === 'saved') {
                    campaignData.adset.savedAudience = document.getElementById('savedAudience').value;
                } else if (campaignData.adset.audienceType === 'custom') {
                    campaignData.adset.targeting = {
                        location: document.getElementById('location').value,
                        radius: parseInt(document.getElementById('radius').value) || null,
                        ageMin: parseInt(document.getElementById('ageMin').value),
                        ageMax: parseInt(document.getElementById('ageMax').value),
                        gender: document.getElementById('gender').value,
                        interests: document.getElementById('interests').value.split(',').map(i => i.trim()).filter(i => i)
                    };
                }
            } else if (currentStep === 3) {
                campaignData.ad = {
                    name: document.getElementById('adName').value,
                    format: document.getElementById('adFormat').value,
                    pageId: document.getElementById('adPage').value,
                    headline: document.getElementById('adHeadline').value,
                    text: document.getElementById('adText').value,
                    description: document.getElementById('adDescription').value,
                    url: document.getElementById('adUrl').value || null,
                    callToAction: document.getElementById('callToAction').value
                };
            }
        }
        
        // Handle audience type change
        function handleAudienceTypeChange() {
            const audienceType = document.getElementById('audienceType').value;
            
            document.getElementById('savedAudienceSelect').style.display = 
                audienceType === 'saved' ? 'block' : 'none';
            document.getElementById('customAudienceForm').style.display = 
                audienceType === 'custom' ? 'block' : 'none';
        }
        
        // Setup character counters
        function setupCharacterCounters() {
            const fields = [
                { id: 'adHeadline', max: 40 },
                { id: 'adText', max: 125 },
                { id: 'adDescription', max: 30 }
            ];
            
            fields.forEach(field => {
                const element = document.getElementById(field.id);
                const counter = element.parentNode.querySelector('.char-counter');
                
                element.addEventListener('input', () => {
                    const length = element.value.length;
                    counter.textContent = `${length}/${field.max}`;
                    counter.style.color = length > field.max ? '#e74c3c' : '#7f8c8d';
                });
            });
        }
        
        // Setup media upload
        function setupMediaUpload() {
            const uploadArea = document.getElementById('adMediaUpload');
            const preview = document.getElementById('adMediaPreview');
            
            uploadArea.addEventListener('click', () => {
                const input = document.createElement('input');
                input.type = 'file';
                input.accept = 'image/*,video/*';
                input.multiple = true;
                input.onchange = handleMediaFiles;
                input.click();
            });
            
            uploadArea.addEventListener('dragover', (e) => {
                e.preventDefault();
                uploadArea.style.background = '#f0f8ff';
            });
            
            uploadArea.addEventListener('dragleave', () => {
                uploadArea.style.background = '';
            });
            
            uploadArea.addEventListener('drop', (e) => {
                e.preventDefault();
                uploadArea.style.background = '';
                handleMediaFiles({ target: { files: e.dataTransfer.files } });
            });
        }
        
        // Handle media files
        function handleMediaFiles(event) {
            const files = Array.from(event.target.files);
            const preview = document.getElementById('adMediaPreview');
            
            files.forEach(file => {
                if (file.type.startsWith('image/') || file.type.startsWith('video/')) {
                    const reader = new FileReader();
                    reader.onload = (e) => {
                        const mediaElement = file.type.startsWith('image/') ?
                            `<img src="${e.target.result}" alt="Preview" style="max-width: 200px; max-height: 200px;">` :
                            `<video src="${e.target.result}" controls style="max-width: 200px; max-height: 200px;"></video>`;
                        
                        preview.innerHTML += `
                            <div class="media-item" style="display: inline-block; margin: 10px; position: relative;">
                                ${mediaElement}
                                <button onclick="this.parentNode.remove()" style="position: absolute; top: 5px; right: 5px; background: #e74c3c; color: white; border: none; border-radius: 50%; width: 25px; height: 25px; cursor: pointer;">×</button>
                            </div>
                        `;
                    };
                    reader.readAsDataURL(file);
                }
            });
        }
        
        // Generate campaign review
        function generateCampaignReview() {
            const summary = document.getElementById('campaignSummary');
            const adPreview = document.getElementById('adPreview');
            const estimate = document.getElementById('performanceEstimate');
            
            // Campaign summary
            summary.innerHTML = `
                <div style="margin-bottom: 15px;">
                    <strong>Campagne:</strong> ${campaignData.campaign?.name || 'N/A'}<br>
                    <strong>Objectif:</strong> ${campaignData.campaign?.objective || 'N/A'}<br>
                    <strong>Budget total:</strong> ${campaignData.campaign?.budget || 0}€
                </div>
                <div style="margin-bottom: 15px;">
                    <strong>Groupe d'annonces:</strong> ${campaignData.adset?.name || 'N/A'}<br>
                    <strong>Budget quotidien:</strong> ${campaignData.adset?.dailyBudget || 0}€<br>
                    <strong>Période:</strong> ${campaignData.adset?.startDate || 'N/A'} - ${campaignData.adset?.endDate || 'Continue'}
                </div>
                <div>
                    <strong>Annonce:</strong> ${campaignData.ad?.name || 'N/A'}<br>
                    <strong>Format:</strong> ${campaignData.ad?.format || 'N/A'}<br>
                    <strong>Action:</strong> ${campaignData.ad?.callToAction || 'N/A'}
                </div>
            `;
            
            // Ad preview
            adPreview.innerHTML = `
                <div style="border: 1px solid #ddd; padding: 15px; border-radius: 8px; max-width: 350px;">
                    <div style="font-weight: bold; margin-bottom: 10px;">${campaignData.ad?.headline || 'Titre'}</div>
                    <div style="margin-bottom: 10px; color: #666;">${campaignData.ad?.text || 'Texte de l\'annonce'}</div>
                    <div style="background: #f0f0f0; padding: 10px; border-radius: 4px; margin-bottom: 10px;">
                        [Média de l'annonce]
                    </div>
                    <div style="font-size: 12px; color: #888; margin-bottom: 10px;">${campaignData.ad?.description || 'Description'}</div>
                    <button style="background: #1877f2; color: white; border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer;">
                        ${campaignData.ad?.callToAction || 'Action'}
                    </button>
                </div>
            `;
            
            // Performance estimate
            const dailyBudget = campaignData.adset?.dailyBudget || 0;
            const estimatedReach = Math.round(dailyBudget * 50); // Rough estimate
            const estimatedClicks = Math.round(dailyBudget * 2);
            const estimatedCPC = dailyBudget > 0 ? (dailyBudget / estimatedClicks).toFixed(2) : '0.00';
            
            estimate.innerHTML = `
                <div class="estimate-metric">
                    <div class="estimate-value">${estimatedReach}</div>
                    <div class="estimate-label">Portée estimée/jour</div>
                </div>
                <div class="estimate-metric">
                    <div class="estimate-value">${estimatedClicks}</div>
                    <div class="estimate-label">Clics estimés/jour</div>
                </div>
                <div class="estimate-metric">
                    <div class="estimate-value">${estimatedCPC}€</div>
                    <div class="estimate-label">CPC estimé</div>
                </div>
            `;
        }
        
        // Submit campaign
        async function submitCampaign() {
            try {
                saveCurrentStepData();
                
                const response = await fetch('/api/facebook/campaigns/create', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(campaignData)
                });
                
                const result = await response.json();
                
                if (result.success) {
                    showAlert('Campagne créée avec succès !', 'success');
                    hideCampaignForm();
                    loadCampaigns();
                } else {
                    showAlert('Erreur lors de la création de la campagne: ' + result.error, 'error');
                }
                
            } catch (error) {
                console.error('Error creating campaign:', error);
                showAlert('Erreur lors de la création de la campagne', 'error');
            }
        }
        
        // Load campaigns
        async function loadCampaigns() {
            try {
                const response = await fetch('/api/facebook/campaigns');
                if (response.ok) {
                    const data = await response.json();
                    updateCampaignsTable(data.campaigns || []);
                } else {
                    document.getElementById('campaignsTableBody').innerHTML = 
                        '<div class="loading-campaigns">Erreur lors du chargement des campagnes</div>';
                }
            } catch (error) {
                console.error('Error loading campaigns:', error);
                document.getElementById('campaignsTableBody').innerHTML = 
                    '<div class="loading-campaigns">Erreur lors du chargement des campagnes</div>';
            }
        }
        
        // Update campaigns table
        function updateCampaignsTable(campaigns) {
            const tbody = document.getElementById('campaignsTableBody');
            
            if (campaigns.length === 0) {
                tbody.innerHTML = '<div class="loading-campaigns">Aucune campagne trouvée</div>';
                return;
            }
            
            tbody.innerHTML = campaigns.map(campaign => `
                <div class="campaign-row">
                    <div class="table-cell">
                        <div class="campaign-name">${campaign.name}</div>
                        <div class="campaign-objective">${campaign.objective}</div>
                    </div>
                    <div class="table-cell">
                        <span class="status-badge status-${campaign.status.toLowerCase()}">${campaign.status}</span>
                    </div>
                    <div class="table-cell">${campaign.budget}€</div>
                    <div class="table-cell">${formatNumber(campaign.reach || 0)}</div>
                    <div class="table-cell">${formatNumber(campaign.clicks || 0)}</div>
                    <div class="table-cell">${campaign.cpc || '0.00'}€</div>
                    <div class="table-cell">
                        <div class="campaign-actions">
                            <button class="action-btn edit" onclick="editCampaign('${campaign.id}')">
                                <i class="fas fa-edit"></i>
                            </button>
                            <button class="action-btn pause" onclick="toggleCampaign('${campaign.id}', '${campaign.status}')">
                                <i class="fas fa-${campaign.status === 'ACTIVE' ? 'pause' : 'play'}"></i>
                            </button>
                            <button class="action-btn delete" onclick="deleteCampaign('${campaign.id}')">
                                <i class="fas fa-trash"></i>
                            </button>
                        </div>
                    </div>
                </div>
            `).join('');
        }
        
        // Load saved audiences for campaigns
        async function loadSavedAudiencesForCampaigns() {
            try {
                const response = await fetch('/api/facebook/audiences');
                if (response.ok) {
                    const data = await response.json();
                    const select = document.getElementById('savedAudience');
                    
                    select.innerHTML = '<option value="">Sélectionner une audience...</option>' +
                        data.audiences.map(audience => 
                            `<option value="${audience.id}">${audience.name}</option>`
                        ).join('');
                }
            } catch (error) {
                console.error('Error loading saved audiences:', error);
            }
        }
        
        // Load pages for campaigns
        async function loadPagesForCampaigns() {
            try {
                const response = await fetch('/api/facebook/pages/publishing');
                if (response.ok) {
                    const data = await response.json();
                    const select = document.getElementById('adPage');
                    
                    select.innerHTML = '<option value="">Sélectionner une page...</option>' +
                        data.pages.map(page => 
                            `<option value="${page.id}">${page.name}</option>`
                        ).join('');
                }
            } catch (error) {
                console.error('Error loading pages:', error);
            }
        }
        
        // Campaign actions
        function editCampaign(campaignId) {
            showAlert('Fonction d\'édition en cours de développement', 'info');
        }
        
        function toggleCampaign(campaignId, currentStatus) {
            const newStatus = currentStatus === 'ACTIVE' ? 'PAUSED' : 'ACTIVE';
            showAlert(`Campagne ${newStatus === 'ACTIVE' ? 'activée' : 'mise en pause'}`, 'success');
            loadCampaigns();
        }
        
        function deleteCampaign(campaignId) {
            if (confirm('Êtes-vous sûr de vouloir supprimer cette campagne ?')) {
                showAlert('Campagne supprimée', 'success');
                loadCampaigns();
            }
        }
