import { create } from 'zustand'

export const useAppStore = create((set, get) => ({
  // UI State
  sidebarOpen: false,
  loading: false,
  
  // Data
  pages: [],
  selectedPages: [],
  
  // Actions
  setSidebarOpen: (open) => set({ sidebarOpen: open }),
  setLoading: (loading) => set({ loading }),
  
  setPages: (pages) => set({ pages }),
  setSelectedPages: (selectedPages) => set({ selectedPages }),
  
  togglePageSelection: (pageId) => {
    const { selectedPages } = get()
    const isSelected = selectedPages.includes(pageId)
    
    if (isSelected) {
      set({ selectedPages: selectedPages.filter(id => id !== pageId) })
    } else {
      set({ selectedPages: [...selectedPages, pageId] })
    }
  },
  
  selectAllPages: () => {
    const { pages } = get()
    set({ selectedPages: pages.map(page => page.id) })
  },
  
  deselectAllPages: () => set({ selectedPages: [] }),
}))