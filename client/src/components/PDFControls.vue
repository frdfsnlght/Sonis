<template>
  <div class="pdf-controls">
  
    <el-dialog
      :visible.sync="dialog"
      title="Perform"
      model
      modal-append-to-body
      append-to-body
    >

      <el-form
        label-width="120px"
      >
      
        <el-form-item label="Zoom">
          <el-slider
            v-model="workingScale"
            show-input
            label="Scale"
            :min="50"
            :max="300"
            :step="10"
            @change="setScale"
          />
        </el-form-item>
        
        <el-form-item label="Document">
          <el-select
            v-model="currentDocumentName"
            placeholder="Select Document"
            @change="setCurrentDocumentName"
          >
            <el-option
              v-for="name in documentNames"
              :key="name"
              :label="name"
              :value="name"
            >
            </el-option>
          </el-select>
        </el-form-item>

      </el-form>
      
    </el-dialog>
    
    <div class="dialogHotspot" @click="dialog = true"/>
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

.dialogHotspot {
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
      dialog: false,
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

