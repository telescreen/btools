<template>
  <table class="table table-sm">
    <thead>
      <tr>
        <th>Name</th>
        <th>Description</th>
        <th>Status</th>
        <th>Session Time</th>
        <th>Created At </th>
        <th>Updated At </th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="(project, idx) in projects">
        <td>
          <router-link :to="{ name: 'project-detail', params: { projectId: project.id } }">
            {{ project.name }}
          </router-link>
        </td>
        <td>{{ project.description }}</td>
        <td>{{ project.status }}</td>
        <td>{{ project.sessionTime }} minutes</td>
        <td>{{ project.createdAt | extractDate }}</td>
        <td>{{ project.updatedAt | extractDate }}</td>
      </tr>
    </tbody>
  </table>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import ProjectService from '@/services/ProjectService';
import { Project } from '@/models/Project';
import { extractDate } from '@/utils';

@Component({
  filters: {
    extractDate,
  },
})
export default class ProjectView extends Vue {
  private projects: Project[] = [];

  private created(): void {
    ProjectService.getAllProjects().then((projectList: Project[]) => {
      this.projects = projectList;
    });
  }
}
</script>
