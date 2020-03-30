import moment from 'moment';
import { keysToCamel } from '@/utils';

interface TaskJSON {
    title: string;
    description: string;
    due_date: string;
    status: number;
    estimated_time: number;
    total_time: number;
    priority: number;
    created_at: string;
    updated_at: string;
    project: number;
}

class Task {
    public static fromJSON(taskJson: TaskJSON): Task {
        return new Task(keysToCamel(taskJson));
    }

    public title: string = '';
    public description: string = '';
    public dueDate: Date = new Date();
    public status: number = 1;
    public estimatedTime: number = 0;
    public totalTime: number = 0;
    public priority: number = 2;
    public createdAt: Date = new Date();
    public updatedAt: Date = new Date();
    public projectId: number = 0;

    constructor(fields?: Partial<Task>) {
        if (fields) {
            Object.assign(this, fields);
        }
    }

    public toJSON(): TaskJSON {
        return {
            title: this.title,
            description: this.description,
            status: this.status,
            priority: this.priority,
            estimated_time: this.estimatedTime,
            total_time: this.totalTime,
            due_date: moment(this.dueDate).format('MM/DD/YYYY HH:mm:ss'),
            created_at: moment(this.createdAt).format('MM/DD/YYYY HH:mm:ss'),
            updated_at: moment(this.updatedAt).format('MM/DD/YYYY HH:mm:ss'),
            project: this.projectId,
        };
    }
}

export { Task, TaskJSON };
