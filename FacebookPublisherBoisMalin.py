"""
Facebook Publisher Bois Malin - Main Application

This is the main application file for the Facebook Publisher Bois Malin tool.
It provides a Tkinter-based GUI for managing Facebook pages, posts, and ads.

Author: Manus AI
Date: June 19, 2025
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import json
import os
from datetime import datetime, timedelta

from facebook_api import FacebookAPI, FacebookAPIError
from models.page import Page
from models.post import Post
from models.ad import AdCreative, Campaign, AdSet, Ad, BoostedPost
from utils import config, scheduler, logger

# Initialize logger
log = logger.get_logger("app")

class FacebookPublisherApp:
    """
    Main application class for Facebook Publisher Bois Malin
    """
    
    def __init__(self, root):
        """
        Initialize the main application window
        
        Args:
            root: Tkinter root window
        """
        self.root = root
        self.root.title("Facebook Publisher Bois Malin")
        self.root.geometry("1000x700")
        
        # Initialize Facebook API (will load from .env)
        try:
            self.fb_api = FacebookAPI()
        except ValueError as e:
            log.error(f"Failed to initialize Facebook API: {e}")
            messagebox.showerror("API Error", f"Failed to initialize Facebook API: {e}\nPlease check your .env file.")
            self.root.destroy()
            return
            
        # Initialize Post Scheduler
        self.post_scheduler = scheduler.PostScheduler(self.fb_api)
        self.post_scheduler.start(on_post_published=self._handle_post_published)
        
        # Load initial data
        self.pages_data = config.load_pages()
        self.scheduled_posts_data = config.load_scheduled_posts()
        self.boosted_ads_data = config.load_boosted_ads()
        
        self.pages: List[Page] = [Page.from_dict(p) for p in self.pages_data.get("pages", [])]
        self.scheduled_posts: List[Post] = [Post.from_dict(p) for p in self.scheduled_posts_data.get("posts", [])]
        self.boosted_ads: List[BoostedPost] = [BoostedPost.from_dict(ad) for ad in self.boosted_ads_data.get("boosted_posts", [])]
        
        # UI Setup
        self._create_widgets()
        self._load_initial_ui_data()
        
        log.info("FacebookPublisherApp initialized")

    def _handle_post_published(self, post: Post):
        """Callback when a scheduled post is published"""
        log.info(f"Scheduled post {post.post_id} published successfully.")
        messagebox.showinfo("Post Published", f"Scheduled post for page(s) {', '.join(post.page_ids)} has been published.")
        # Refresh UI if needed (e.g., update scheduled posts list)
        self._refresh_scheduled_posts_tab()

    def _create_widgets(self):
        """Create all UI widgets"""
        self.notebook = ttk.Notebook(self.root)
        
        # Create tabs
        self.tab_publication = ttk.Frame(self.notebook)
        self.tab_programmation = ttk.Frame(self.notebook)
        self.tab_publicites = ttk.Frame(self.notebook)
        self.tab_statistiques = ttk.Frame(self.notebook)
        self.tab_parametres = ttk.Frame(self.notebook)
        self.tab_a_propos = ttk.Frame(self.notebook)
        
        self.notebook.add(self.tab_publication, text="Publication")
        self.notebook.add(self.tab_programmation, text="Programmation")
        self.notebook.add(self.tab_publicites, text="Publicités")
        self.notebook.add(self.tab_statistiques, text="Statistiques")
        self.notebook.add(self.tab_parametres, text="Paramètres")
        self.notebook.add(self.tab_a_propos, text="À Propos")
        
        self.notebook.pack(expand=True, fill="both")
        
        # Populate tabs
        self._create_publication_tab()
        self._create_programmation_tab()
        self.setup_ads_tab()
        self._create_statistiques_tab()
        self._create_parametres_tab()
        self._create_a_propos_tab()

    def _load_initial_ui_data(self):
        """Load initial data into UI elements"""
        # Example: Load pages into a listbox in parameters tab
        self._refresh_pages_list_parametres()
        self._refresh_scheduled_posts_tab()
        # ... and other tabs

    # --- Publication Tab --- #
    def _create_publication_tab(self):
        """Create widgets for the Publication tab"""
        # Message entry
        ttk.Label(self.tab_publication, text="Message:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.publication_message_text = tk.Text(self.tab_publication, height=10, width=80)
        self.publication_message_text.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")
        
        # Link entry
        ttk.Label(self.tab_publication, text="Lien (optionnel):").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.publication_link_entry = ttk.Entry(self.tab_publication, width=80)
        self.publication_link_entry.grid(row=2, column=1, columnspan=2, padx=5, pady=5, sticky="ew")
        
        # Media selection
        ttk.Label(self.tab_publication, text="Média:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.publication_media_path_var = tk.StringVar()
        ttk.Entry(self.tab_publication, textvariable=self.publication_media_path_var, width=60, state="readonly").grid(row=3, column=1, padx=5, pady=5, sticky="ew")
        ttk.Button(self.tab_publication, text="Ajouter une image", command=self._select_image_publication).grid(row=3, column=2, padx=5, pady=5)
        # TODO: Add video support if needed
        
        # Page selection
        ttk.Label(self.tab_publication, text="Pages:").grid(row=4, column=0, padx=5, pady=5, sticky="nw")
        self.publication_pages_listbox = tk.Listbox(self.tab_publication, selectmode=tk.MULTIPLE, height=10, exportselection=False)
        self.publication_pages_listbox.grid(row=4, column=1, columnspan=2, padx=5, pady=5, sticky="nsew")
        # Populate with pages from self.pages
        for page in self.pages:
            self.publication_pages_listbox.insert(tk.END, page.name)
            
        # Publish button
        ttk.Button(self.tab_publication, text="Publier maintenant", command=self._publish_now).grid(row=5, column=1, padx=5, pady=10)
        ttk.Button(self.tab_publication, text="Programmer...", command=self._open_schedule_dialog).grid(row=5, column=2, padx=5, pady=10)
        
        # Configure row/column weights for resizing
        self.tab_publication.grid_rowconfigure(1, weight=1)
        self.tab_publication.grid_rowconfigure(4, weight=1)
        self.tab_publication.grid_columnconfigure(1, weight=1)

    def _select_image_publication(self):
        """Open file dialog to select an image for publication"""
        filepath = filedialog.askopenfilename(
            title="Sélectionner une image",
            filetypes=(("Images JPEG", "*.jpg *.jpeg"), ("Images PNG", "*.png"), ("Tous les fichiers", "*.*"))
        )
        if filepath:
            self.publication_media_path_var.set(filepath)

    def _publish_now(self):
        """Handle immediate post publication"""
        message = self.publication_message_text.get("1.0", tk.END).strip()
        link = self.publication_link_entry.get().strip()
        media_path = self.publication_media_path_var.get().strip()
        selected_indices = self.publication_pages_listbox.curselection()
        
        if not message and not media_path:
            messagebox.showerror("Erreur", "Le message ou un média est requis.")
            return
            
        if not selected_indices:
            messagebox.showerror("Erreur", "Veuillez sélectionner au moins une page.")
            return
            
        selected_pages = [self.pages[i] for i in selected_indices]
        
        try:
            for page in selected_pages:
                page_token = page.access_token
                if not page_token:
                    # Attempt to get from main token if page token is missing (should be rare)
                    page_token = self.fb_api.access_token 
                    log.warning(f"Using system user token for page {page.id} as page-specific token is missing.")
                
                if media_path:
                    # Upload photo first
                    photo_response = self.fb_api.upload_photo(page.id, media_path, caption=message, published=False, page_access_token=page_token)
                    photo_id = photo_response.get("id")
                    if not photo_id:
                        raise FacebookAPIError("Échec de l'upload de la photo.")
                    # Publish post with attached photo
                    post_response = self.fb_api.publish_post_with_photos(page.id, message, [photo_id], page_access_token=page_token)
                else:
                    # Publish text/link post
                    post_response = self.fb_api.publish_post(page.id, message, link, page_access_token=page_token)
                
                post_id = post_response.get("id")
                log.info(f"Post {post_id} published to page {page.id} ({page.name})")
                # TODO: Offer to open post in browser
                # TODO: Add to a "recent posts" list for boosting
                
            messagebox.showinfo("Succès", "Publication effectuée avec succès sur les pages sélectionnées.")
            # Clear fields
            self.publication_message_text.delete("1.0", tk.END)
            self.publication_link_entry.delete(0, tk.END)
            self.publication_media_path_var.set("")
            
        except FacebookAPIError as e:
            log.error(f"API Error during publication: {e}")
            messagebox.showerror("Erreur API", f"Erreur lors de la publication : {e.message}")
        except Exception as e:
            log.error(f"Unexpected error during publication: {e}")
            messagebox.showerror("Erreur Inattendue", f"Une erreur inattendue s'est produite : {e}")

    def _open_schedule_dialog(self):
        """Open dialog to schedule a post"""
        message = self.publication_message_text.get("1.0", tk.END).strip()
        link = self.publication_link_entry.get().strip()
        media_path = self.publication_media_path_var.get().strip()
        selected_indices = self.publication_pages_listbox.curselection()

        if not message and not media_path:
            messagebox.showerror("Erreur", "Le message ou un média est requis pour programmer.")
            return

        if not selected_indices:
            messagebox.showerror("Erreur", "Veuillez sélectionner au moins une page pour programmer.")
            return

        selected_page_ids = [self.pages[i].id for i in selected_indices]

        # Simple dialog for date and time
        # In a real app, use a calendar widget
        schedule_str = simpledialog.askstring("Programmer la publication", 
                                              "Entrez la date et l'heure (YYYY-MM-DD HH:MM):")
        if not schedule_str:
            return

        try:
            scheduled_time = datetime.strptime(schedule_str, "%Y-%m-%d %H:%M")
            if scheduled_time <= datetime.now():
                messagebox.showerror("Erreur", "La date de programmation doit être dans le futur.")
                return

            new_post = Post(
                message=message,
                page_ids=selected_page_ids,
                link=link if link else None,
                image_paths=[media_path] if media_path else [],
                scheduled_time=scheduled_time
            )
            
            if self.post_scheduler.add_scheduled_post(new_post):
                messagebox.showinfo("Succès", f"Publication programmée pour {scheduled_time.strftime('%Y-%m-%d %H:%M')}.")
                self._refresh_scheduled_posts_tab()
                # Clear fields
                self.publication_message_text.delete("1.0", tk.END)
                self.publication_link_entry.delete(0, tk.END)
                self.publication_media_path_var.set("")
            else:
                messagebox.showerror("Erreur", "Échec de la programmation de la publication.")

        except ValueError:
            messagebox.showerror("Erreur de Format", "Format de date invalide. Utilisez YYYY-MM-DD HH:MM.")
        except Exception as e:
            log.error(f"Error scheduling post: {e}")
            messagebox.showerror("Erreur Inattendue", f"Erreur lors de la programmation : {e}")

    # --- Programmation Tab --- #
    def _create_programmation_tab(self):
        """Create widgets for the Programmation tab"""
        ttk.Label(self.tab_programmation, text="Publications programmées:").pack(padx=5, pady=5, anchor="w")
        
        self.programmation_tree = ttk.Treeview(self.tab_programmation, 
                                               columns=("message", "pages", "time", "status"), 
                                               show="headings")
        self.programmation_tree.heading("message", text="Message")
        self.programmation_tree.heading("pages", text="Pages")
        self.programmation_tree.heading("time", text="Heure programmée")
        self.programmation_tree.heading("status", text="Statut")
        self.programmation_tree.pack(expand=True, fill="both", padx=5, pady=5)
        
        ttk.Button(self.tab_programmation, text="Supprimer la sélection", command=self._delete_scheduled_post).pack(pady=5)
        ttk.Button(self.tab_programmation, text="Actualiser", command=self._refresh_scheduled_posts_tab).pack(pady=5)

    def _refresh_scheduled_posts_tab(self):
        """Refresh the list of scheduled posts in the UI"""
        # Clear existing items
        for item in self.programmation_tree.get_children():
            self.programmation_tree.delete(item)
            
        # Load posts from scheduler
        self.scheduled_posts = self.post_scheduler.get_scheduled_posts()
        for i, post in enumerate(self.scheduled_posts):
            status = "Publié" if post.published else ("En attente" if post.scheduled_time else "Erreur")
            if post.scheduled_time and not post.published and post.scheduled_time < datetime.now():
                status = "En retard"
            
            self.programmation_tree.insert("", tk.END, iid=str(i), values=(
                post.message[:50] + "..." if len(post.message) > 50 else post.message,
                ", ".join(post.page_ids),
                post.scheduled_time.strftime("%Y-%m-%d %H:%M") if post.scheduled_time else "N/A",
                status
            ))

    def _delete_scheduled_post(self):
        """Delete the selected scheduled post"""
        selected_item = self.programmation_tree.focus()
        if not selected_item:
            messagebox.showwarning("Aucune sélection", "Veuillez sélectionner une publication à supprimer.")
            return

        if messagebox.askyesno("Confirmer la suppression", "Êtes-vous sûr de vouloir supprimer cette publication programmée ?"):
            try:
                index = int(selected_item) # Assuming iid is the index
                if self.post_scheduler.remove_scheduled_post(index):
                    messagebox.showinfo("Succès", "Publication programmée supprimée.")
                    self._refresh_scheduled_posts_tab()
                else:
                    messagebox.showerror("Erreur", "Impossible de supprimer la publication programmée.")
            except ValueError:
                 messagebox.showerror("Erreur", "Sélection invalide pour la suppression.")
            except Exception as e:
                log.error(f"Error deleting scheduled post: {e}")
                messagebox.showerror("Erreur Inattendue", f"Erreur lors de la suppression : {e}")

    # --- Publicités Tab --- #
    def setup_ads_tab(self):
        """Create widgets for the Publicités tab according to specifications"""
        ads_frame = ttk.Frame(self.tab_publicites)
        ads_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Configure grid weights for responsive design
        ads_frame.grid_columnconfigure(0, weight=1)
        ads_frame.grid_rowconfigure(5, weight=1)  # Treeview row
        
        # ROW 0 - AdAccount & Page selectors
        selectors_frame = ttk.LabelFrame(ads_frame, text="Sélection Compte et Page")
        selectors_frame.grid(row=0, column=0, sticky="nsew", pady=(0, 10))
        selectors_frame.grid_columnconfigure(1, weight=1)
        
        ttk.Label(selectors_frame, text="Compte Publicitaire:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.combo_act = ttk.Combobox(selectors_frame, state="readonly", width=40, postcommand=self.refresh_ad_accounts)
        self.combo_act.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        ttk.Label(selectors_frame, text="Page Facebook:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.combo_page_ads = ttk.Combobox(selectors_frame, state="readonly", width=40, postcommand=self.refresh_pages_ads)
        self.combo_page_ads.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        
        # ROW 1 - Objective / Budget / Dates
        config_frame = ttk.LabelFrame(ads_frame, text="Configuration de Campagne")
        config_frame.grid(row=1, column=0, sticky="nsew", pady=(0, 10))
        config_frame.grid_columnconfigure(1, weight=1)
        config_frame.grid_columnconfigure(3, weight=1)
        
        ttk.Label(config_frame, text="Objectif:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.combo_objective = ttk.Combobox(config_frame, state="readonly", values=["POST_ENGAGEMENT", "TRAFFIC", "CONVERSIONS", "REACH"])
        self.combo_objective.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.combo_objective.set("POST_ENGAGEMENT")  # Default value
        
        ttk.Label(config_frame, text="Budget quotidien (€):").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.entry_budget = ttk.Entry(config_frame, width=15)
        self.entry_budget.grid(row=0, column=3, padx=5, pady=5, sticky="w")
        self.entry_budget.insert(0, "20")  # Default budget
        
        ttk.Label(config_frame, text="Date début:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_start = ttk.Entry(config_frame, width=15)
        self.entry_start.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.entry_start.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        ttk.Label(config_frame, text="Date fin:").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.entry_end = ttk.Entry(config_frame, width=15)
        self.entry_end.grid(row=1, column=3, padx=5, pady=5, sticky="w")
        self.entry_end.insert(0, (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"))
        
        # ROW 2 - Targeting
        targeting_frame = ttk.LabelFrame(ads_frame, text="Ciblage")
        targeting_frame.grid(row=2, column=0, sticky="nsew", pady=(0, 10))
        targeting_frame.grid_columnconfigure(1, weight=1)
        targeting_frame.grid_columnconfigure(3, weight=1)
        
        ttk.Label(targeting_frame, text="Pays:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_country = ttk.Entry(targeting_frame, width=15)
        self.entry_country.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.entry_country.insert(0, "FR")  # Default country
        
        ttk.Label(targeting_frame, text="Âge min:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.entry_age_min = ttk.Entry(targeting_frame, width=10)
        self.entry_age_min.grid(row=0, column=3, padx=5, pady=5, sticky="w")
        self.entry_age_min.insert(0, "18")
        
        ttk.Label(targeting_frame, text="Âge max:").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.entry_age_max = ttk.Entry(targeting_frame, width=10)
        self.entry_age_max.grid(row=1, column=3, padx=5, pady=5, sticky="w")
        self.entry_age_max.insert(0, "65")
        
        # ROW 3 - Creative inputs
        creative_frame = ttk.LabelFrame(ads_frame, text="Créatif Publicitaire")
        creative_frame.grid(row=3, column=0, sticky="nsew", pady=(0, 10))
        creative_frame.grid_columnconfigure(0, weight=1)
        
        ttk.Label(creative_frame, text="Message publicitaire:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_ad_message = tk.Text(creative_frame, height=4, width=60)
        self.entry_ad_message.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        
        image_frame = ttk.Frame(creative_frame)
        image_frame.grid(row=2, column=0, padx=5, pady=5, sticky="ew")
        image_frame.grid_columnconfigure(1, weight=1)
        
        ttk.Label(image_frame, text="Image:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.selected_ad_image_var = tk.StringVar()
        ttk.Entry(image_frame, textvariable=self.selected_ad_image_var, state="readonly").grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.btn_select_image = ttk.Button(image_frame, text="Choisir image", command=self.select_ad_image)
        self.btn_select_image.grid(row=0, column=2, padx=5, pady=5)
        
        # ROW 4 - Buttons
        buttons_frame = ttk.Frame(ads_frame)
        buttons_frame.grid(row=4, column=0, sticky="ew", pady=(0, 10))
        
        ttk.Button(buttons_frame, text="Créer Campagne", command=self.create_campaign_flow).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Créer Publicité", command=self.create_ad_flow).pack(side="left", padx=5)
        
        # ROW 5 - Treeview ads
        tree_frame = ttk.LabelFrame(ads_frame, text="Campagnes et Publicités Créées")
        tree_frame.grid(row=5, column=0, sticky="nsew")
        tree_frame.grid_columnconfigure(0, weight=1)
        tree_frame.grid_rowconfigure(0, weight=1)
        
        # Create Treeview
        columns = ("campaign_id", "adset_id", "ad_id", "name", "objective", "budget", "status")
        self.tree_ads = ttk.Treeview(tree_frame, columns=columns, show="headings")
        
        # Define headings
        self.tree_ads.heading("campaign_id", text="Campaign ID")
        self.tree_ads.heading("adset_id", text="AdSet ID")
        self.tree_ads.heading("ad_id", text="Ad ID")
        self.tree_ads.heading("name", text="Nom")
        self.tree_ads.heading("objective", text="Objectif")
        self.tree_ads.heading("budget", text="Budget")
        self.tree_ads.heading("status", text="Statut")
        
        # Configure column widths
        self.tree_ads.column("campaign_id", width=100)
        self.tree_ads.column("adset_id", width=100)
        self.tree_ads.column("ad_id", width=100)
        self.tree_ads.column("name", width=150)
        self.tree_ads.column("objective", width=120)
        self.tree_ads.column("budget", width=80)
        self.tree_ads.column("status", width=80)
        
        # Add scrollbar
        scrollbar_ads = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree_ads.yview)
        self.tree_ads.configure(yscrollcommand=scrollbar_ads.set)
        
        # Pack treeview and scrollbar
        self.tree_ads.grid(row=0, column=0, sticky="nsew")
        scrollbar_ads.grid(row=0, column=1, sticky="ns")
        
        # Initialize variables
        self.selected_ad_image = None
        self.current_campaign_id = None
        
        # Load existing ads from JSON
        self._load_ads_from_json()
        
        # --- Creative Configuration Frame -----------------
        creative_frame = ttk.LabelFrame(main_frame, text="Créatif Publicitaire")
        creative_frame.pack(fill="x", pady=(0, 10))
        
        # Message
        ttk.Label(creative_frame, text="Message publicitaire:").grid(row=0, column=0, padx=5, pady=5, sticky="nw")
        self.ads_message_text = tk.Text(creative_frame, height=4, width=60)
        self.ads_message_text.grid(row=0, column=1, columnspan=2, padx=5, pady=5, sticky="ew")
        
        # Link
        ttk.Label(creative_frame, text="Lien de destination:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.ads_link_entry = ttk.Entry(creative_frame, width=50)
        self.ads_link_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        
        # Image
        ttk.Label(creative_frame, text="Image:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.ads_media_path_var = tk.StringVar()
        ttk.Entry(creative_frame, textvariable=self.ads_media_path_var, width=40, state="readonly").grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        ttk.Button(creative_frame, text="Choisir image", command=self._select_image_ads).grid(row=2, column=2, padx=5, pady=5)
        
        # CTA
        ttk.Label(creative_frame, text="Appel à l'action:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.combo_cta = ttk.Combobox(creative_frame, state="readonly", width=20)
        self.combo_cta["values"] = ["LEARN_MORE", "SHOP_NOW", "SIGN_UP", "DOWNLOAD", "CONTACT_US", "CALL_NOW"]
        self.combo_cta.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        
        creative_frame.grid_columnconfigure(1, weight=1)
        
        # --- Action buttons -----------------------------
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Button(buttons_frame, text="Créer Campagne", command=self._create_campaign_flow).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Créer Publicité Complète", command=self._create_ad_flow).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Actualiser Liste", command=self._refresh_ads_list).pack(side="right", padx=5)
        
        # --- Treeview of ads ----------------------------
        ads_list_frame = ttk.LabelFrame(main_frame, text="Publicités et Campagnes")
        ads_list_frame.pack(fill="both", expand=True)
        
        # Create Treeview
        columns = ("id", "name", "status", "objective", "budget")
        self.tree_ads = ttk.Treeview(ads_list_frame, columns=columns, show="headings", height=8)
        
        # Define headings
        self.tree_ads.heading("id", text="ID")
        self.tree_ads.heading("name", text="Nom")
        self.tree_ads.heading("status", text="Statut")
        self.tree_ads.heading("objective", text="Objectif")
        self.tree_ads.heading("budget", text="Budget")
        
        # Configure column widths
        self.tree_ads.column("id", width=100)
        self.tree_ads.column("name", width=200)
        self.tree_ads.column("status", width=100)
        self.tree_ads.column("objective", width=150)
        self.tree_ads.column("budget", width=100)
        
        # Add scrollbar
        scrollbar_ads = ttk.Scrollbar(ads_list_frame, orient="vertical", command=self.tree_ads.yview)
        self.tree_ads.configure(yscrollcommand=scrollbar_ads.set)
        
        # Pack treeview and scrollbar
        self.tree_ads.pack(side="left", fill="both", expand=True)
        scrollbar_ads.pack(side="right", fill="y")
        
        # Initialize data
        self._refresh_ad_accounts()
        self._refresh_ads_pages_combo()

    # --- Statistiques Tab --- #
    def _create_statistiques_tab(self):
        """Create widgets for the Statistiques tab"""
        # Main container
        main_frame = ttk.Frame(self.tab_statistiques)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # --- Page and Date Selection Frame ---
        selection_frame = ttk.LabelFrame(main_frame, text="Sélection et Période")
        selection_frame.pack(fill="x", pady=(0, 10))
        
        # Page selector
        ttk.Label(selection_frame, text="Page:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.combo_stats_pages = ttk.Combobox(selection_frame, state="readonly", width=40)
        self.combo_stats_pages.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        # Date range
        ttk.Label(selection_frame, text="Du:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.entry_date_from = ttk.Entry(selection_frame, width=12)
        self.entry_date_from.insert(0, (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d"))
        self.entry_date_from.grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Label(selection_frame, text="Au:").grid(row=0, column=4, padx=5, pady=5, sticky="w")
        self.entry_date_to = ttk.Entry(selection_frame, width=12)
        self.entry_date_to.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.entry_date_to.grid(row=0, column=5, padx=5, pady=5)
        
        ttk.Button(selection_frame, text="Actualiser", command=self.refresh_stats).grid(row=0, column=6, padx=5, pady=5)
        
        selection_frame.grid_columnconfigure(1, weight=1)
        
        # --- Page Statistics Frame ---
        page_stats_frame = ttk.LabelFrame(main_frame, text="Statistiques de la Page")
        page_stats_frame.pack(fill="x", pady=(0, 10))
        
        # Create labels for page stats
        ttk.Label(page_stats_frame, text="Impressions:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.label_page_impressions = ttk.Label(page_stats_frame, text="0", font=("Arial", 12, "bold"))
        self.label_page_impressions.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        ttk.Label(page_stats_frame, text="Utilisateurs engagés:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.label_page_engaged = ttk.Label(page_stats_frame, text="0", font=("Arial", 12, "bold"))
        self.label_page_engaged.grid(row=0, column=3, padx=5, pady=5, sticky="w")
        
        ttk.Label(page_stats_frame, text="Portée:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.label_page_reach = ttk.Label(page_stats_frame, text="0", font=("Arial", 12, "bold"))
        self.label_page_reach.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        
        ttk.Label(page_stats_frame, text="Fans:").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.label_page_fans = ttk.Label(page_stats_frame, text="0", font=("Arial", 12, "bold"))
        self.label_page_fans.grid(row=1, column=3, padx=5, pady=5, sticky="w")
        
        # --- Recent Posts Frame ---
        posts_frame = ttk.LabelFrame(main_frame, text="Publications Récentes")
        posts_frame.pack(fill="both", expand=True)
        
        # Create Treeview for recent posts
        posts_columns = ("id", "message", "date", "impressions", "engagement")
        self.tree_recent_posts = ttk.Treeview(posts_frame, columns=posts_columns, show="headings", height=8)
        
        # Define headings
        self.tree_recent_posts.heading("id", text="ID Post")
        self.tree_recent_posts.heading("message", text="Message")
        self.tree_recent_posts.heading("date", text="Date")
        self.tree_recent_posts.heading("impressions", text="Impressions")
        self.tree_recent_posts.heading("engagement", text="Engagement")
        
        # Configure column widths
        self.tree_recent_posts.column("id", width=100)
        self.tree_recent_posts.column("message", width=300)
        self.tree_recent_posts.column("date", width=100)
        self.tree_recent_posts.column("impressions", width=100)
        self.tree_recent_posts.column("engagement", width=100)
        
        # Add scrollbar for posts
        scrollbar_posts = ttk.Scrollbar(posts_frame, orient="vertical", command=self.tree_recent_posts.yview)
        self.tree_recent_posts.configure(yscrollcommand=scrollbar_posts.set)
        
        # Pack posts treeview and scrollbar
        self.tree_recent_posts.pack(side="left", fill="both", expand=True)
        scrollbar_posts.pack(side="right", fill="y")
        
        # --- Boost Post Button ---
        boost_frame = ttk.Frame(main_frame)
        boost_frame.pack(fill="x", pady=(5, 0))
        
        self.btn_boost = ttk.Button(boost_frame, text="Booster ce post", command=self.boost_selected_post)
        self.btn_boost.pack(side="left", padx=5)
        ttk.Button(boost_frame, text="Voir détails", command=self._show_post_details).pack(side="left", padx=5)
        
        # Initialize data
        self._refresh_stats_pages_combo()

    # --- Paramètres Tab --- #
    def _create_parametres_tab(self):
        """Create widgets for the Paramètres tab"""
        param_frame = ttk.LabelFrame(self.tab_parametres, text="Configuration Facebook")
        param_frame.pack(padx=10, pady=10, fill="x")

        # Token Management
        ttk.Label(param_frame, text="Token d'accès système actuel:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.system_token_var = tk.StringVar(value=self.fb_api.access_token if self.fb_api.access_token else "Non défini")
        ttk.Entry(param_frame, textvariable=self.system_token_var, width=70, state="readonly").grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        ttk.Label(param_frame, text="Nouveau token système:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.new_system_token_entry = ttk.Entry(param_frame, width=70)
        self.new_system_token_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        ttk.Button(param_frame, text="Mettre à jour token système", command=self._update_system_token).grid(row=1, column=2, padx=5, pady=5)

        ttk.Button(param_frame, text="Échanger token court terme", command=self._exchange_token).grid(row=2, column=1, padx=5, pady=5, sticky="w")
        ttk.Button(param_frame, text="Vérifier validité token système", command=self._debug_system_token).grid(row=2, column=2, padx=5, pady=5, sticky="w")
        self.token_expiry_label = ttk.Label(param_frame, text="Expiration du token: N/A")
        self.token_expiry_label.grid(row=3, column=1, columnspan=2, padx=5, pady=5, sticky="w")

        # Page Management
        pages_frame = ttk.LabelFrame(self.tab_parametres, text="Gestion des Pages")
        pages_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        ttk.Button(pages_frame, text="Actualiser la liste des pages Facebook", command=self._refresh_facebook_pages).pack(pady=5)
        self.parametres_pages_listbox = tk.Listbox(pages_frame, height=15, width=80)
        self.parametres_pages_listbox.pack(padx=5, pady=5, fill="both", expand=True)
        # TODO: Display page ID and page-specific token status

    def _update_system_token(self):
        """Update the system user access token"""
        new_token = self.new_system_token_entry.get().strip()
        if not new_token:
            messagebox.showerror("Erreur", "Veuillez entrer un nouveau token.")
            return
        
        # Update in fb_api instance
        self.fb_api.access_token = new_token
        # Update display
        self.system_token_var.set(new_token)
        # Save to .env (This is tricky, as .env is usually not modified by the app itself)
        # For now, this change is only for the current session.
        # A more robust solution would involve a config file or secure storage.
        log.info("System token updated for current session.")
        messagebox.showinfo("Token Mis à Jour", "Le token système a été mis à jour pour la session actuelle.")
        self._debug_system_token() # Check new token

    def _exchange_token(self):
        """Exchange a short-lived token for a long-lived one"""
        short_token = simpledialog.askstring("Échanger Token", "Entrez le token court terme:")
        if not short_token:
            return
        try:
            response = self.fb_api.exchange_token(short_token)
            long_token = response.get("access_token")
            if long_token:
                self.new_system_token_entry.delete(0, tk.END)
                self.new_system_token_entry.insert(0, long_token)
                messagebox.showinfo("Succès", f"Token long terme obtenu: {long_token[:30]}...")
                self._update_system_token() # Update with the new long-lived token
            else:
                messagebox.showerror("Erreur", f"Échec de l'échange du token: {response}")
        except FacebookAPIError as e:
            log.error(f"API Error during token exchange: {e}")
            messagebox.showerror("Erreur API", f"Erreur lors de l'échange du token : {e.message}")
        except Exception as e:
            log.error(f"Unexpected error during token exchange: {e}")
            messagebox.showerror("Erreur Inattendue", f"Une erreur inattendue s'est produite : {e}")

    def _debug_system_token(self):
        """Debug the current system token and display expiry"""
        if not self.fb_api.access_token:
            self.token_expiry_label.config(text="Expiration du token: Aucun token système défini.")
            return
        try:
            response = self.fb_api.debug_token(self.fb_api.access_token)
            data = response.get("data", {})
            if data.get("is_valid"):
                expires_at = data.get("expires_at")
                if expires_at and expires_at != 0:
                    expiry_dt = datetime.fromtimestamp(expires_at)
                    self.token_expiry_label.config(text=f"Expiration du token: {expiry_dt.strftime('%Y-%m-%d %H:%M:%S')}")
                    # Check for expiry warning
                    if expiry_dt - datetime.now() < timedelta(days=7):
                        messagebox.showwarning("Expiration Proche", "Votre token Facebook va expirer dans moins de 7 jours!")
                else:
                    self.token_expiry_label.config(text="Expiration du token: N'expire pas (ou inconnu).")
            else:
                error_msg = data.get("error", {}).get("message", "Token invalide.")
                self.token_expiry_label.config(text=f"Expiration du token: {error_msg}")
                messagebox.showerror("Token Invalide", error_msg)
        except FacebookAPIError as e:
            log.error(f"API Error during token debug: {e}")
            self.token_expiry_label.config(text=f"Expiration du token: Erreur API - {e.message}")
            messagebox.showerror("Erreur API", f"Erreur lors de la vérification du token : {e.message}")
        except Exception as e:
            log.error(f"Unexpected error during token debug: {e}")
            self.token_expiry_label.config(text=f"Expiration du token: Erreur inattendue - {e}")
            messagebox.showerror("Erreur Inattendue", f"Une erreur inattendue s'est produite : {e}")

    def _refresh_facebook_pages(self):
        """Refresh the list of Facebook pages from the API"""
        try:
            pages_response = self.fb_api.get_user_pages()
            self.pages = [Page.from_api_response(p) for p in pages_response]
            
            # Save pages to JSON
            pages_to_save = {"pages": [p.to_dict() for p in self.pages]}
            config.save_pages(pages_to_save)
            
            # Update UI elements
            self._refresh_pages_list_parametres()
            self._refresh_pages_list_publication()
            
            messagebox.showinfo("Succès", f"{len(self.pages)} pages Facebook récupérées et sauvegardées.")
        except FacebookAPIError as e:
            log.error(f"API Error refreshing pages: {e}")
            messagebox.showerror("Erreur API", f"Erreur lors de la récupération des pages : {e.message}")
        except Exception as e:
            log.error(f"Unexpected error refreshing pages: {e}")
            messagebox.showerror("Erreur Inattendue", f"Une erreur inattendue s'est produite : {e}")

    def _refresh_pages_list_parametres(self):
        """Refresh the pages list in the Paramètres tab"""
        self.parametres_pages_listbox.delete(0, tk.END)
        for page in self.pages:
            self.parametres_pages_listbox.insert(tk.END, f"{page.name} (ID: {page.id})")

    def _refresh_pages_list_publication(self):
        """Refresh the pages list in the Publication tab"""
        self.publication_pages_listbox.delete(0, tk.END)
        for page in self.pages:
            self.publication_pages_listbox.insert(tk.END, page.name)

    # --- À Propos Tab --- #
    def _create_a_propos_tab(self):
        """Create widgets for the À Propos tab"""
        ttk.Label(self.tab_a_propos, text="Facebook Publisher Bois Malin", font=("Helvetica", 16, "bold")).pack(pady=10)
        ttk.Label(self.tab_a_propos, text="Version 2.0 (API Intégrée)").pack(pady=5)
        ttk.Label(self.tab_a_propos, text="Développé par Manus AI pour Nicolas Pycik").pack(pady=5)
        ttk.Label(self.tab_a_propos, text="© 2025").pack(pady=5)
        # TODO: Add more details from README.md or link to it

    def on_closing(self):
        """Handle window closing event"""
        log.info("Closing application...")
        if self.post_scheduler:
            self.post_scheduler.stop()
        self.root.destroy()

    # --- Publicités Backend Methods --- #
    def _refresh_ad_accounts(self):
        """Refresh the list of ad accounts"""
        try:
            accounts = self.fb_api.get_ad_accounts()
            account_names = [f"{acc.get('name', 'Unknown')} ({acc.get('id', '')})" for acc in accounts]
            self.combo_ad_accounts["values"] = account_names
            
            # Store mapping for later use
            self.ad_account_map = {acc.get('name', 'Unknown'): acc.get('id', '') for acc in accounts}
            
            if account_names:
                self.combo_ad_accounts.current(0)
                log.info(f"Loaded {len(accounts)} ad accounts")
            else:
                log.warning("No ad accounts found")
                
        except Exception as e:
            log.error(f"Error refreshing ad accounts: {e}")
            messagebox.showerror("Erreur", f"Impossible de charger les comptes publicitaires: {e}")

    def _refresh_ads_pages_combo(self):
        """Refresh the pages combo for ads tab"""
        try:
            pages_data = config.load_pages()
            pages = pages_data.get("pages", [])
            page_names = [f"{page['name']} ({page['id']})" for page in pages]
            self.combo_ads_pages["values"] = page_names
            
            if page_names:
                self.combo_ads_pages.current(0)
                
        except Exception as e:
            log.error(f"Error refreshing ads pages: {e}")

    def _load_ads_from_json(self):
        """Load existing ads from JSON file"""
        try:
            ads_file = os.path.join(self.data_dir, "ads_created.json")
            if os.path.exists(ads_file):
                with open(ads_file, 'r', encoding='utf-8') as f:
                    ads_data = json.load(f)
                    
                # Clear existing items
                self.tree_ads.delete(*self.tree_ads.get_children())
                
                # Add ads to treeview
                for ad in ads_data:
                    self.tree_ads.insert("", "end", values=(
                        ad.get("campaign_id", ""),
                        ad.get("adset_id", ""),
                        ad.get("ad_id", ""),
                        ad.get("name", ""),
                        ad.get("objective", ""),
                        ad.get("daily_budget", ""),
                        "PAUSED"
                    ))
        except Exception as e:
            log.error(f"Error loading ads from JSON: {e}")

    def _save_ad_to_json(self, campaign_id: str, adset_id: str, ad_id: str, name: str, objective: str, daily_budget: int):
        """Save created ad to JSON file"""
        try:
            ads_file = os.path.join(self.data_dir, "ads_created.json")
            
            # Load existing data
            ads_data = []
            if os.path.exists(ads_file):
                with open(ads_file, 'r', encoding='utf-8') as f:
                    ads_data = json.load(f)
            
            # Add new ad
            new_ad = {
                "campaign_id": campaign_id,
                "adset_id": adset_id,
                "ad_id": ad_id,
                "name": name,
                "objective": objective,
                "daily_budget": daily_budget,
                "created_time": datetime.now().isoformat()
            }
            ads_data.append(new_ad)
            
            # Save back to file
            with open(ads_file, 'w', encoding='utf-8') as f:
                json.dump(ads_data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            log.error(f"Error saving ad to JSON: {e}")

    def select_ad_image(self):
        """Select image for ads creative"""
        file_path = filedialog.askopenfilename(
            title="Choisir une image",
            filetypes=[("Images", "*.jpg *.jpeg *.png *.gif")]
        )
        if file_path:
            self.selected_ad_image_var.set(file_path)
            self.selected_ad_image = file_path

    def refresh_ad_accounts(self):
        """Refresh the list of ad accounts"""
        try:
            ad_accounts = self.api.get_ad_accounts()
            account_names = []
            
            for account in ad_accounts:
                name = account.get("name", f"Account {account['id']}")
                account_id = account["id"]
                account_names.append(f"{name} ({account_id})")
            
            self.combo_act["values"] = account_names
            if account_names:
                self.combo_act.current(0)
                
        except Exception as e:
            log.error(f"Error refreshing ad accounts: {e}")
            messagebox.showerror("Erreur", f"Impossible de récupérer les comptes publicitaires: {e}")

    def refresh_pages_ads(self):
        """Refresh the list of pages for ads tab"""
        try:
            pages = self.api.get_user_pages()
            page_names = []
            
            for page in pages:
                name = page.get("name", f"Page {page['id']}")
                page_id = page["id"]
                page_names.append(f"{name} ({page_id})")
            
            self.combo_page_ads["values"] = page_names
            if page_names:
                self.combo_page_ads.current(0)
                
        except Exception as e:
            log.error(f"Error refreshing pages for ads: {e}")

    def _selected_account_id(self) -> str:
        """Get the selected ad account ID"""
        sel = self.combo_act.get()
        if not sel:
            return ""
        return sel.split("(")[-1].strip(")")

    def _selected_ads_page(self) -> str:
        """Get the selected page ID from ads tab"""
        sel = self.combo_page_ads.get()
        if not sel:
            return ""
        return sel.split("(")[-1].strip(")")

    def _build_targeting(self) -> dict:
        """Build targeting object from form inputs"""
        return {
            "geo_locations": {"countries": [self.entry_country.get() or "FR"]},
            "age_min": int(self.entry_age_min.get() or "18"),
            "age_max": int(self.entry_age_max.get() or "65")
        }

    def create_campaign_flow(self):
        """Create a campaign according to specifications"""
        try:
            act = self._selected_account_id()
            if not act:
                messagebox.showerror("Erreur", "Veuillez sélectionner un compte publicitaire")
                return
                
            name = f"Campagne {datetime.now():%Y%m%d%H%M}"
            obj = self.combo_objective.get() or "POST_ENGAGEMENT"
            
            camp = self.api.create_campaign(act, name, obj)
            messagebox.showinfo("Campagne", f"Créée : {camp['id']}")
            self.current_campaign_id = camp["id"]
            
        except Exception as e:
            log.error(f"Error creating campaign: {e}")
            messagebox.showerror("Erreur", f"Erreur lors de la création de campagne: {e}")

    def create_ad_flow(self):
        """Create complete ad workflow: creative → campaign → adset → ad"""
        try:
            act = self._selected_account_id()
            page_id = self._selected_ads_page()
            
            if not act or not page_id:
                messagebox.showerror("Erreur", "Veuillez sélectionner un compte publicitaire et une page")
                return
            
            # Create campaign if not exists
            if not self.current_campaign_id:
                name = f"Campagne {datetime.now():%Y%m%d%H%M}"
                obj = self.combo_objective.get() or "POST_ENGAGEMENT"
                camp = self.api.create_campaign(act, name, obj)
                self.current_campaign_id = camp["id"]
            
            # Upload image if provided
            creative_id = None
            if self.selected_ad_image:
                photo = self.api.upload_photo(page_id, self.selected_ad_image)
                creative = self.api.create_ad_creative(
                    act, 
                    object_story_id=None,
                    photo_hash=photo["id"],
                    message=self.entry_ad_message.get("1.0", "end").strip()
                )
                creative_id = creative["id"]
            else:
                # Create simple creative
                creative = self.api.create_ad_creative(act, f"{page_id}_dummy")
                creative_id = creative["id"]

            # Create adset
            adset = self.api.create_ad_set(
                act, 
                f"AdSet {datetime.now():%H%M%S}",
                self.current_campaign_id,
                daily_budget=int(self.entry_budget.get() or "20") * 100,  # to cents
                targeting=self._build_targeting()
            )

            # Create ad
            ad = self.api.create_ad(
                act, 
                f"Ad {datetime.now():%H%M%S}",
                adset["id"], 
                creative_id
            )
            
            # Save to JSON and update treeview
            self._save_ad_to_json(
                self.current_campaign_id,
                adset["id"],
                ad["id"],
                f"Ad {datetime.now():%H%M%S}",
                self.combo_objective.get() or "POST_ENGAGEMENT",
                int(self.entry_budget.get() or "20")
            )
            
            # Add to treeview
            self.tree_ads.insert("", "end", values=(
                self.current_campaign_id,
                adset["id"],
                ad["id"],
                f"Ad {datetime.now():%H%M%S}",
                self.combo_objective.get() or "POST_ENGAGEMENT",
                self.entry_budget.get() or "20",
                "PAUSED"
            ))
            
            messagebox.showinfo("Publicité", f"Publicité créée : {ad['id']}")
            
        except Exception as e:
            log.error(f"Error creating ad: {e}")
            messagebox.showerror("Erreur", f"Erreur lors de la création de publicité: {e}")

    def _get_selected_ad_account_id(self):
        """Get the selected ad account ID"""
        selection = self.combo_ad_accounts.get()
        if not selection:
            return None
        
        # Extract ID from "Name (ID)" format
        if "(" in selection and ")" in selection:
            return selection.split("(")[-1].replace(")", "")
        return None

    def _get_selected_ads_page_id(self):
        """Get the selected page ID from ads tab"""
        selection = self.combo_ads_pages.get()
        if not selection:
            return None
        
        # Extract ID from "Name (ID)" format
        if "(" in selection and ")" in selection:
            return selection.split("(")[-1].replace(")", "")
        return None

    def _create_campaign_flow(self):
        """Create a new campaign"""
        try:
            # Get form data
            act_id = self._get_selected_ad_account_id()
            if not act_id:
                messagebox.showerror("Erreur", "Veuillez sélectionner un compte publicitaire")
                return
            
            name = self.entry_campaign_name.get().strip()
            if not name:
                messagebox.showerror("Erreur", "Veuillez entrer un nom de campagne")
                return
            
            objective = self.combo_objective.get()
            if not objective:
                messagebox.showerror("Erreur", "Veuillez sélectionner un objectif")
                return
            
            # Create campaign
            campaign = self.fb_api.create_campaign(act_id, name, objective)
            
            # Add to tree view
            self.tree_ads.insert("", "end", values=(
                campaign.get("id", ""),
                name,
                "PAUSED",
                objective,
                "N/A"
            ))
            
            messagebox.showinfo("Succès", f"Campagne créée avec l'ID: {campaign.get('id')}")
            log.info(f"Campaign created: {campaign.get('id')}")
            
        except Exception as e:
            log.error(f"Error creating campaign: {e}")
            messagebox.showerror("Erreur", f"Erreur lors de la création de la campagne: {e}")

    def _create_ad_flow(self):
        """Create a complete ad (campaign + adset + ad + creative)"""
        try:
            # Validate inputs
            act_id = self._get_selected_ad_account_id()
            page_id = self._get_selected_ads_page_id()
            
            if not act_id:
                messagebox.showerror("Erreur", "Veuillez sélectionner un compte publicitaire")
                return
            
            if not page_id:
                messagebox.showerror("Erreur", "Veuillez sélectionner une page")
                return
            
            name = self.entry_campaign_name.get().strip()
            objective = self.combo_objective.get()
            budget = self.entry_daily_budget.get().strip()
            message = self.ads_message_text.get("1.0", tk.END).strip()
            
            if not all([name, objective, budget, message]):
                messagebox.showerror("Erreur", "Veuillez remplir tous les champs obligatoires")
                return
            
            try:
                budget_int = int(float(budget) * 100)  # Convert to cents
            except ValueError:
                messagebox.showerror("Erreur", "Budget invalide")
                return
            
            # Build targeting
            targeting = {
                "geo_locations": {"countries": [self.entry_location.get() or "FR"]},
                "age_min": int(self.entry_age_min.get() or 18),
                "age_max": int(self.entry_age_max.get() or 65)
            }
            
            # 1. Create campaign
            campaign = self.fb_api.create_campaign(act_id, name, objective)
            campaign_id = campaign.get("id")
            
            # 2. Create adset
            adset = self.fb_api.create_adset(
                act_id, campaign_id, budget_int, 
                targeting=targeting
            )
            adset_id = adset.get("id")
            
            # 3. Create creative
            creative_data = {
                "name": f"Creative for {name}",
                "object_story_spec": {
                    "page_id": page_id,
                    "link_data": {
                        "message": message,
                        "link": self.ads_link_entry.get() or "",
                        "call_to_action": {
                            "type": self.combo_cta.get() or "LEARN_MORE"
                        }
                    }
                }
            }
            
            # Add image if selected
            image_path = self.ads_media_path_var.get()
            if image_path:
                # Upload image first
                image_hash = self.fb_api.upload_image(act_id, image_path)
                creative_data["object_story_spec"]["link_data"]["image_hash"] = image_hash
            
            creative = self.fb_api.create_ad_creative(act_id, creative_data)
            creative_id = creative.get("id")
            
            # 4. Create ad
            ad = self.fb_api.create_ad(act_id, f"Ad for {name}", adset_id, creative_id)
            
            # Add to tree view
            self.tree_ads.insert("", "end", values=(
                ad.get("id", ""),
                name,
                "PAUSED",
                objective,
                f"{budget}€/jour"
            ))
            
            messagebox.showinfo("Succès", 
                f"Publicité complète créée!\n"
                f"Campagne: {campaign_id}\n"
                f"Ensemble de pub: {adset_id}\n"
                f"Publicité: {ad.get('id')}")
            
            log.info(f"Complete ad created: {ad.get('id')}")
            
        except Exception as e:
            log.error(f"Error creating complete ad: {e}")
            messagebox.showerror("Erreur", f"Erreur lors de la création de la publicité: {e}")

    def _refresh_ads_list(self):
        """Refresh the list of ads and campaigns"""
        try:
            # Clear existing items
            for item in self.tree_ads.get_children():
                self.tree_ads.delete(item)
            
            # This would require additional API calls to get campaigns/ads
            # For now, just show a message
            log.info("Ads list refresh requested")
            
        except Exception as e:
            log.error(f"Error refreshing ads list: {e}")

    # --- Statistics Backend Methods --- #
    def _refresh_stats_pages_combo(self):
        """Refresh the pages combo for stats tab"""
        try:
            pages_data = config.load_pages()
            pages = pages_data.get("pages", [])
            page_names = [f"{page['name']} ({page['id']})" for page in pages]
            self.combo_stats_pages["values"] = page_names
            
            if page_names:
                self.combo_stats_pages.current(0)
                
        except Exception as e:
            log.error(f"Error refreshing stats pages: {e}")

    def _get_selected_stats_page_id(self):
        """Get the selected page ID from stats tab"""
        selection = self.combo_stats_pages.get()
        if not selection:
            return None
        
        # Extract ID from "Name (ID)" format
        if "(" in selection and ")" in selection:
            return selection.split("(")[-1].replace(")", "")
        return None

    def refresh_stats(self):
        """Refresh statistics according to specifications"""
        try:
            page_id = self._selected_stats_page()
            if not page_id:
                messagebox.showerror("Erreur", "Veuillez sélectionner une page")
                return
            
            # Calculate date range (30 days by default)
            since = int((datetime.now() - timedelta(days=30)).timestamp())
            until = int(datetime.now().timestamp())
            
            # Get page insights with real API calls
            try:
                ins = self.api.get_page_insights(page_id, since, until)
                
                # Extract metrics according to specifications
                reach = "N/A"
                engaged = "N/A"
                
                for metric in ins:
                    if metric["name"] == "page_impressions" and metric["values"]:
                        reach = metric["values"][0]["value"]
                    elif metric["name"] == "page_engaged_users" and metric["values"]:
                        engaged = metric["values"][0]["value"]
                
                # Update labels
                self.label_page_impressions.config(text=str(reach))
                self.label_page_engaged.config(text=str(engaged))
                
            except Exception as e:
                log.warning(f"Could not get page insights: {e}")
                self.label_page_impressions.config(text="N/A")
                self.label_page_engaged.config(text="N/A")
            
            # Get recent posts with real API calls
            try:
                posts = self.api.get_recent_posts(page_id)
                
                # Clear existing posts
                self.tree_recent_posts.delete(*self.tree_recent_posts.get_children())
                
                # Add posts to treeview according to specifications
                for p in posts:
                    post_id = p.get("id", "")
                    message = p.get("message", "")[:40]  # Limit to 40 chars
                    created_time = p.get("created_time", "")
                    
                    self.tree_recent_posts.insert("", "end", values=(post_id, message, created_time))
                    
            except Exception as e:
                log.warning(f"Could not get recent posts: {e}")
                self.tree_recent_posts.delete(*self.tree_recent_posts.get_children())
                
        except Exception as e:
            log.error(f"Error refreshing stats: {e}")
            messagebox.showerror("Erreur", f"Erreur lors de l'actualisation des statistiques: {e}")

    def _selected_stats_page(self) -> str:
        """Get the selected page ID from stats tab"""
        sel = self.combo_stats_pages.get()
        if not sel:
            return ""
        return sel.split("(")[-1].strip(")")

    def _refresh_stats(self):
        """Refresh statistics for the selected page and date range"""
        try:
            page_id = self._get_selected_stats_page_id()
            if not page_id:
                messagebox.showerror("Erreur", "Veuillez sélectionner une page")
                return
            
            # Parse dates
            try:
                date_from = datetime.strptime(self.entry_date_from.get(), "%Y-%m-%d")
                date_to = datetime.strptime(self.entry_date_to.get(), "%Y-%m-%d")
                since = int(date_from.timestamp())
                until = int(date_to.timestamp())
            except ValueError:
                messagebox.showerror("Erreur", "Format de date invalide (YYYY-MM-DD)")
                return
            
            # Get page insights
            try:
                insights = self.fb_api.get_page_insights(page_id, since, until)
                
                # Update page stats labels
                if insights and "data" in insights:
                    for metric in insights["data"]:
                        metric_name = metric.get("name", "")
                        values = metric.get("values", [])
                        
                        if values and "value" in values[0]:
                            value = values[0]["value"]
                            
                            if metric_name == "page_impressions":
                                self.label_page_impressions.config(text=str(value))
                            elif metric_name == "page_engaged_users":
                                self.label_page_engaged.config(text=str(value))
                
                # Set default values for missing metrics
                if not any(m.get("name") == "page_impressions" for m in insights.get("data", [])):
                    self.label_page_impressions.config(text="N/A")
                if not any(m.get("name") == "page_engaged_users" for m in insights.get("data", [])):
                    self.label_page_engaged.config(text="N/A")
                    
            except Exception as e:
                log.warning(f"Could not get page insights: {e}")
                self.label_page_impressions.config(text="N/A")
                self.label_page_engaged.config(text="N/A")
            
            # Get recent posts
            try:
                posts = self.fb_api.get_page_posts(page_id, limit=10)
                
                # Clear existing posts
                for item in self.tree_recent_posts.get_children():
                    self.tree_recent_posts.delete(item)
                
                # Add posts to tree
                for post in posts:
                    post_id = post.get("id", "")
                    message = post.get("message", "")[:50] + "..." if len(post.get("message", "")) > 50 else post.get("message", "")
                    created_time = post.get("created_time", "")
                    
                    # Try to get post insights
                    try:
                        post_insights = self.fb_api.get_post_insights(post_id)
                        impressions = "N/A"
                        engagement = "N/A"
                        
                        if post_insights and "data" in post_insights:
                            for metric in post_insights["data"]:
                                if metric.get("name") == "post_impressions":
                                    values = metric.get("values", [])
                                    if values and "value" in values[0]:
                                        impressions = str(values[0]["value"])
                                elif metric.get("name") == "post_engaged_users":
                                    values = metric.get("values", [])
                                    if values and "value" in values[0]:
                                        engagement = str(values[0]["value"])
                    except:
                        impressions = "N/A"
                        engagement = "N/A"
                    
                    # Format date
                    try:
                        if created_time:
                            dt = datetime.fromisoformat(created_time.replace("Z", "+00:00"))
                            formatted_date = dt.strftime("%Y-%m-%d")
                        else:
                            formatted_date = "N/A"
                    except:
                        formatted_date = "N/A"
                    
                    self.tree_recent_posts.insert("", "end", values=(
                        post_id,
                        message,
                        formatted_date,
                        impressions,
                        engagement
                    ))
                    
            except Exception as e:
                log.warning(f"Could not get page posts: {e}")
            
            log.info(f"Stats refreshed for page {page_id}")
            
        except Exception as e:
            log.error(f"Error refreshing stats: {e}")
            messagebox.showerror("Erreur", f"Erreur lors de l'actualisation des statistiques: {e}")

    def boost_selected_post(self):
        """Boost the selected post according to specifications"""
        try:
            # Get selected post
            sel = self.tree_recent_posts.selection()
            if not sel:
                messagebox.showerror("Erreur", "Veuillez sélectionner un post à booster")
                return
                
            post_id = self.tree_recent_posts.item(sel[0])["values"][0]  # col0=id
            page_id = post_id.split("_")[0]

            # Ask for ad account selection
            act_id = self.ask_ad_account_dialog()
            if not act_id:
                return  # User cancelled
                
            # Create boost workflow: creative → campaign → adset → ad
            creative = self.api.create_ad_creative(act_id, post_id)
            camp = self.api.create_campaign(act_id, f"Boost {post_id}", "POST_ENGAGEMENT")
            adset = self.api.create_ad_set(
                act_id, 
                f"Boost AdSet {post_id}",
                camp["id"], 
                daily_budget=2000,  # 20€ in cents
                targeting={"geo_locations": {"countries": ["FR"]}, "age_min": 18, "age_max": 65}
            )
            ad = self.api.create_ad(act_id, f"Boost {post_id}", adset["id"], creative["id"])
            
            messagebox.showinfo("Boost", f"Publicité créée : {ad['id']}")
            
        except Exception as e:
            log.error(f"Error boosting post: {e}")
            messagebox.showerror("Erreur", f"Erreur lors du boost: {e}")

    def ask_ad_account_dialog(self) -> str:
        """Pop-up dialog to select ad account for boost"""
        try:
            ad_accounts = self.api.get_ad_accounts()
            
            if not ad_accounts:
                messagebox.showerror("Erreur", "Aucun compte publicitaire trouvé")
                return ""
                
            if len(ad_accounts) == 1:
                # Only one account, use it automatically
                return ad_accounts[0]["id"]
            
            # Multiple accounts, show selection dialog
            dialog = tk.Toplevel(self.root)
            dialog.title("Sélectionner un compte publicitaire")
            dialog.geometry("400x200")
            dialog.transient(self.root)
            dialog.grab_set()
            
            # Center the dialog
            dialog.update_idletasks()
            x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
            y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
            dialog.geometry(f"+{x}+{y}")
            
            selected_account = tk.StringVar()
            
            ttk.Label(dialog, text="Choisissez un compte publicitaire pour le boost:").pack(pady=10)
            
            # Create listbox with accounts
            listbox = tk.Listbox(dialog, height=6)
            listbox.pack(fill="both", expand=True, padx=20, pady=10)
            
            for account in ad_accounts:
                name = account.get("name", f"Account {account['id']}")
                listbox.insert(tk.END, f"{name} ({account['id']})")
            
            listbox.selection_set(0)  # Select first by default
            
            def on_ok():
                selection = listbox.curselection()
                if selection:
                    account_text = listbox.get(selection[0])
                    account_id = account_text.split("(")[-1].replace(")", "")
                    selected_account.set(account_id)
                dialog.destroy()
            
            def on_cancel():
                dialog.destroy()
            
            # Buttons
            button_frame = ttk.Frame(dialog)
            button_frame.pack(pady=10)
            
            ttk.Button(button_frame, text="OK", command=on_ok).pack(side="left", padx=5)
            ttk.Button(button_frame, text="Annuler", command=on_cancel).pack(side="left", padx=5)
            
            # Wait for dialog to close
            dialog.wait_window()
            
            return selected_account.get()
            
        except Exception as e:
            log.error(f"Error in ad account dialog: {e}")
            messagebox.showerror("Erreur", f"Erreur lors de la sélection du compte: {e}")
            return ""

    def _show_post_details(self):
        """Show details of the selected post"""
        try:
            # Get selected post
            selection = self.tree_recent_posts.selection()
            if not selection:
                messagebox.showerror("Erreur", "Veuillez sélectionner un post")
                return
            
            values = self.tree_recent_posts.item(selection[0], "values")
            post_id = values[0]
            message = values[1] if len(values) > 1 else "N/A"
            created_time = values[2] if len(values) > 2 else "N/A"
            
            # Show details in popup
            details = f"ID: {post_id}\n\nMessage: {message}\n\nDate: {created_time}"
            messagebox.showinfo("Détails du post", details)
            
        except Exception as e:
            log.error(f"Error showing post details: {e}")
            messagebox.showerror("Erreur", f"Erreur lors de l'affichage des détails: {e}")


if __name__ == "__main__":
    # This file should be run via main.py for proper imports
    print("Please run the application using: python main.py")
    print("This ensures proper module imports and initialization.")

