<template>
  <div class="pdf-controls">
    <v-navigation-drawer
      v-model="drawer"
      absolute
      dark
      temporary
      right
    >
      <v-list class="pa-1">
        <v-list-tile @click.stop="drawer = !drawer">
          <v-list-tile-action>
            <v-icon>chevron_right</v-icon>
          </v-list-tile-action>
        </v-list-tile>

        <v-slider
          label="Scale"
          min="50"
          max="300"
          step="10"
          thumb-label="always"
          v-model="workingScale"
          @end="setScale"
        >
        </v-slider>
        
        <v-list-group
          prepend-icon="account_circle"
          v-model="expandDocs"
        >
          <v-list-tile slot="activator">
            <v-list-tile-title>Documents</v-list-tile-title>
          </v-list-tile>

          <v-list-tile
            v-for="name in documentNames"
              :key="name"
              @click="setCurrentDocumentName(name)"
              avatar
            >
            <v-list-tile-avatar>
              <v-icon v-if="name == currentDocumentName">check</v-icon>
            </v-list-tile-avatar>
            <v-list-tile-title v-text="name"></v-list-tile-title>
          </v-list-tile>
            
        </v-list-group>

      </v-list>
    </v-navigation-drawer>
    
    <div class="drawerHotspot" @click="drawer = !drawer"/>
    <div class="nextPageHotspot" @click="nextPage"/>
    <div class="previousPageHotspot" @click="previousPage"/>
    
  </div>
</template>

<style scoped>

.pdf-controls {
  background-color: transparent;
  z-index: 10;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  overflow: clip;
}

.drawerHotspot {
  position: absolute;
  top: 0;
  right: 0;
  width: 1in;
  height: 1in;
  /*background-color: #300030;*/
}

.nextPageHotspot {
  position: absolute;
  top: 1in;
  right: 0;
  width: 1in;
  height: 12in;
  /*background-color: #300030;*/
}

.previousPageHotspot {
  position: absolute;
  top: 1in;
  left: 0;
  width: 1in;
  height: 12in;
  /*background-color: #300030;*/
}

</style>

<script>

export default {

  name: 'PDFControls',
  
  props: {
  
    documentName: {
      type: String,
      default: null,
    },
    
    scale: {
      type: Number,
      default: 1.0,
    },
    
  },
  
  data() {
    return {
      drawer: false,
      expandDocs: false,
      documentNames: [
        'anger a.pdf',
        'anger a Violoncello 1.pdf',
        'anger b section.pdf',
        'anger b section Violoncello 1 anger b.pdf',
        'CanonVlVc.pdf',
        'HalloweenVlVc.pdf',
        'Mozart Requiem.pdf',
        'Purcell No 6.score.mus.pdf',
        'tear drops Violoncello 1.pdf',
        'Vacant.pdf',
        'valse anna.pdf',
        'valse anna Violoncello 1.pdf',
        'WeddingVlVc.pdf',
      ],
      currentDocumentName: this.documentName,
      currentScale: Math.floor(this.scale * 100),
      workingScale: Math.floor(this.scale * 100),
    };
  },
  
  watch: {
  
    documentName(name) {
      this.setCurrentDocumentName(name)
    },
    
    scale(scale) {
      this.setCurrentScale(scale)
    },
    
    currentDocumentName(name) {
      this.$emit('documentChanged', name)
    },
    
    currentScale(scale) {
      this.$emit('scaleChanged', scale / 100.0)
    },
    
  },
  
  
  methods: {
  
    setCurrentDocumentName(name) {
      this.drawer = false
      this.currentDocumentName = name
    },
    
    setScale() {
      this.currentScale = this.workingScale
    },
    
    setCurrentScale(scale) {
      this.currentScale = Math.floor(scale * 100)
    },
    
    nextPage() {
      console.log('nextPage')
    },
    
    previousPage() {
      console.log('previousPage')
    },
    
  },

  created() {
  },

  
}

</script>

