<style scoped>

.pdf-page {
}

</style>

<script>

export default {

  name: 'PDFPage',
  
  props: {
    page: {
      type: Object,
      required: true,
    },
    scale: {
      type: Number,
      default: 1.0,
    }
  },

  data() {
    return {
      viewport: this.page.getViewport(this.scale),
      renderTask: null,
    };
  },
  
  render(h) {
    return h('canvas', {attrs: this.canvasAttrs})
  },  
  
  watch: {
  
    page(page, oldPage) {
      this.destroyPage(oldPage)
    },
    
    scale(scale) {
      this.viewport = this.page.getViewport(scale)
      this.drawPage()
    },
    
  },
  
  computed: {

    canvasAttrs() {
      const width = this.viewport.width
      const height = this.viewport.height
      const pixelRatio = window.devicePixelRatio || 1
      const pixelWidth = Math.ceil(width / pixelRatio)
      const pixelHeight = Math.ceil(height / pixelRatio)
      return {
        width: Math.ceil(this.viewport.width),
        height: Math.ceil(this.viewport.height),
        style: `width: ${pixelWidth}px; height: ${pixelHeight}px;`,
        class: 'pdf-page',
      }
    },
      
  },
  
  methods: {

    drawPage() {
      if (this.renderTask) {
        this.destroyRenderTask()
      }
      //return

      const canvasContext = this.$el.getContext('2d')
      const renderContext = {canvasContext, viewport: this.viewport}

      console.time('page ' + this.page.pageNumber)
      this.renderTask = this.page.render(renderContext)
      this.renderTask.then(() => {
        console.timeEnd('page ' + this.page.pageNumber)
        this.$emit('rendered', this.page)
        this.renderTask = null
      }).catch(this.destroyRenderTask)
    },
    
    destroyPage(page) {
      if (! page) return
      page._destroy()
      this.destroyRenderTask()
    },

    destroyRenderTask() {
      if (! this.renderTask) return
      this.renderTask.cancel()
      this.renderTask = null
    },
    
  },

  mounted() {
    this.drawPage()
  },
  
  beforeDestroy() {
    this.destroyPage(this.page)
  },
  
}

</script>

