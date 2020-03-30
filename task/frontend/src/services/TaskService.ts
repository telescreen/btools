import 'jquery';

import { Project } from '@/models/Project';
import { Task } from '@/models/Task';
import ServiceStatus from './ServiceStatus';

export default class ProjectService {
  public static ENDPOINT: string = '/task-manage/api/tasks/';

  public static createTask(projectId: number, task: Task): Promise<ServiceStatus> {
    return new Promise<ServiceStatus>((resolve, reject) => {
      $.ajax({
        type: 'POST',
        url: ProjectService.ENDPOINT,
        data: task.toJSON(),
      }).done((response) => {
          const status = new ServiceStatus(response.code, response.message);
          resolve(status);
      });
    });
  }
}
