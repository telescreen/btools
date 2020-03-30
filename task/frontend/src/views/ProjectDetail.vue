<template>
  <ProjectDetailComponent :projectId="projectId"></ProjectDetailComponent>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import ProjectDetailComponent from '@/components/ProjectDetailComponent.vue';

@Component({
  components: {
    ProjectDetailComponent,
  },
})
export default class ProjectDetailView extends Vue {
  @Prop()
  private projectId!: number;
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
</style>
