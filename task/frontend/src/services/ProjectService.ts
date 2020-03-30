import 'jquery';

import { Project } from '@/models/Project';
import { Task } from '@/models/Task';
import ServiceStatus from './ServiceStatus';

export default class ProjectService {
  public static ENDPOINT: string = '/task-manage/api/projects/';

  public static getAllProjects(): Promise<Project[]> {
    return new Promise<Project[]>((resolve, reject) => {
      $.ajax(ProjectService.ENDPOINT).done((response) => {
        const projects: Project[] = [];
        response.results.forEach((elem: any) => projects.push(Project.fromJSON(elem)));
        resolve(projects);
      }).fail((error) => {
        console.log(error);
        reject(error);
      });
    });
  }

  public static getProject(projectId: number): Promise<Project> {
    return new Promise<Project>((resolve, reject) => {
      $.ajax(ProjectService.ENDPOINT + projectId + '/').done((response) => {
        resolve(new Project(Project.fromJSON(response)));
      }).fail((error) => {
        console.log(error);
        reject(error);
      });
   });
  }
}
