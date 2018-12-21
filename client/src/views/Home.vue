<template>
  <div class="home">
    <PDFDocument :doc="doc" :scale="scale" />
    <PDFControls
      :documentName="doc"
      :scale="scale"
      @documentChanged="setDocument"
      @scaleChanged="setScale"
    />
  </div>
</template>

<style scoped>

.home {
  position: relative;
  background-color: #000000;
  height: 100vh;
  width: 100vw;
}

</style>

<script>
// @ is an alias to /src
import PDFDocument from '@/components/PDFDocument.vue'
import PDFControls from '@/components/PDFControls.vue'

export default {
  name: 'Home',
  
  data() {
    return {
      doc: null,
      scale: 2,
    }
  },
  
  components: {
    PDFDocument,
    PDFControls,
  },
  
  methods: {
  
    setDocument(doc) {
      console.log('setDocument: ' + doc)
      this.doc = doc
    },
    
    setScale(scale) {
      this.scale = scale
    },
  
  }
  
}
</script>
