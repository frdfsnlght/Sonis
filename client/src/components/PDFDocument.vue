<template>
  <div class="pdf-document">
    <PDFPage
      v-for="page in pages"
      :key="page.pageNumber"
      :page="page"
      :scale="scale"
    />
  </div>
</template>

<style scoped>

.pdf-document {
  /*background-color: #000000;*/
  text-align: center;
}

</style>

<script>

import pdfjs from 'pdfjs-dist/webpack'
import PDFPage from '@/components/PDFPage.vue'
import server from '../server'

export default {

  name: 'PDFDocument',
  
  props: ['doc', 'scale'],

  data() {
    return {
      pdf: undefined,
      pages: [],
    };
  },
  
  components: {
    PDFPage
  },
  
  watch: {
  
    doc() {
      this.fetchPDF()
    },
    
    pdf(pdf) {
      this.pages = []
      let promises = []
      if (pdf) {
        console.time('getPages')
        for (let i = 1; i <= pdf.numPages; i++)
          promises.push(pdf.getPage(i))
        Promise.all(promises).then(pages => {
          console.timeEnd('getPages')
          this.pages = pages
        })
      } else {
        this.pages = []
      }
    },
    
  },
  
  methods: {
  
    fetchPDF() {
      if (this.doc) {
        console.time('fetchPDF')
        pdfjs.getDocument(server.uri() + '/documents/' + this.doc).then(pdf => {
          console.timeEnd('fetchPDF')
          this.pdf = pdf
        })
      } else {
        this.pdf = null
      }
    },
    
  },

  created() {
    this.fetchPDF()
  },

  
}

</script>

