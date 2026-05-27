import vuex from 'vuex'
import vue from 'vue'

vue.use(vuex)

const state={
  userRole:null,
  currentUser: JSON.parse(localStorage.getItem('authUser') || 'null'),
  userMenus: JSON.parse(localStorage.getItem('userMenus') || '[]')
}

const mutations={
  SetRole(state,val){
    state.userRole=val
  },
  SetCurrentUser(state, user) {
    state.currentUser = user
  },
  SetUserMenus(state, menus) {
    state.userMenus = menus || []
    localStorage.setItem('userMenus', JSON.stringify(state.userMenus))
  },
  ClearCurrentUser(state) {
    state.currentUser = null
    state.userRole = null
    state.userMenus = []
    localStorage.removeItem('userMenus')
  }
}

export default new vuex.Store({
  state,
  mutations
})
