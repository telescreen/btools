<template>
  <div class="container">
    <div class="row m-1">
      <div class="col-md-10">
        <h4>All Tasks </h4>
      </div>
      <div class="col-md-2">
        <button type="button" class="btn btn-sm btn-success" data-toggle="modal" data-target="#CreateTaskModal">+ Create Task</button>
      </div>
    </div>

    <table class="table table-sm">
      <thead>
        <tr>
          <th>Title</th>
          <th>Description</th>
          <th>Status</th>
          <th>Due Date</th>
          <th>Estimated Time</th>
          <th>Total Time</th>
          <th>Priority</th>
          <th>Created At </th>
          <th>Updated At </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(task, idx) in tasks">
          <td>{{ task.title }}</td>
          <td>{{ task.description }}</td>
          <td>{{ task.status }}</td>
          <td>{{ task.dueDate | extractDate }}</td>
          <td>{{ task.estimatedTime }} minutes</td>
          <td>{{ task.totalTime }} minutes</td>
          <td>{{ task.priority }} minutes</td>
          <td>{{ task.createdAt | extractDate }}</td>
          <td>{{ task.updatedAt | extractDate }}</td>
        </tr>
      </tbody>
    </table>

     <!-- Modal to create tasks -->
    <div class="modal fade" id="CreateTaskModal" tabindex="-1" role="dialog">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Create a new Task</h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <form class="form">
            <div class="modal-body">
              <div class="form-group">
                <label for="taskTitle">Title</label>
                <input type="text" class="form-control" id="taskTitle"
                        aria-describedby="taskTitle" placeholder="Task Title"
                        v-model="newTask.title">
              </div>
              <div class="form-group">
                <label for="taskDescription">Description</label>
                <textarea class="form-control" id="taskDescription"
                          aria-describedby="taskDescription" placeholder="Task Details"
                          v-model="newTask.description"></textarea>
              </div>
              <div class="form-group">
                <label for="taskStatus">Status</label>
                <select class="form-control" id="taskStatus" v-model="newTask.status">
                  <option value="1">New</option>
                  <option value="2">Doing</option>
                  <option value="3">Done</option>
                </select>
              </div>
              <div class="form-group">
                <label for="taskDueDate">Deadline Date</label>
                <Datepicker id="taskDueDate" v-model="newTask.dueDate" format="yyyy/MM/dd"></Datepicker>
              </div>
              <div class="form-group">
                <label for="taskEstimatedTime">Estimated Time (Minutes)</label>
                <input type="text" class="form-control" id="taskEstimatedTime"
                        aria-describedby="taskEstimatedTime" placeholder="Estimated Time"
                        v-model="newTask.estimatedTime">
              </div>
              <div class="form-group">
                <label for="taskPriority">Task Priority</label>
                <select class="form-control" id="taskPriority" v-model="newTask.priority">
                  <option value="1">Low</option>
                  <option value="2">Middle</option>
                  <option value="3">High</option>
                </select>
              </div>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
              <button type="button" class="btn btn-primary" @click="createNewTask">Save</button>
            </div>
          </form>
        </div>
      </div>
    </div> <!-- End Modal to create tasks -->

  </div> <!-- End Container -->
</template>

<script lang="ts">
import 'jquery';
import { Component, Prop, Vue } from 'vue-property-decorator';
import Datepicker from 'vuejs-datepicker';

import { extractDate } from '@/utils';
import ProjectService from '@/services/ProjectService';
import TaskService from '@/services/TaskService';
import ServiceStatus from '@/services/ServiceStatus';

import { Project } from '@/models/Project';
import { Task } from '@/models/Task';

@Component({
  filters: {
    extractDate,
  },
  components: {
    Datepicker,
  },
})
export default class ProjectDetailComponent extends Vue {
  @Prop()
  private projectId!: number;

  private project!: Project;

  private tasks: Task[] = [];

  private newTask: Task = new Task();

  private taskModal = $('#CreateTaskModal');

  private created() {
    ProjectService.getProject(this.projectId).then((project: Project) => {
      this.project = project;
      this.tasks = Object.assign([], project.tasks);
    });
  }

  private createNewTask() {
    this.newTask.projectId = this.projectId;
    TaskService.createTask(this.projectId, this.newTask).then((status: ServiceStatus) => {
        console.log(status);
    });
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
</style>
