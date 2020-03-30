import { Task } from './Task';
import moment from 'moment';
import { keysToCamel } from '@/utils';

interface ProjectJSON {
    id: number;
    name: string;
    description: string;
    status: string;
    session_time: number;
    created_at: string;
    updated_at: string;
    tasks?: Task[];
}

class Project {
    public static fromJSON(taskJson: ProjectJSON): Project {
        return new Project(keysToCamel(taskJson));
    }

    public id: number = 0;
    public name: string = '';
    public description: string = '';
    public status: string = '';
    public sessionTime: number = 0;
    public createdAt: string = '';
    public updatedAt: string = '';
    public tasks?: Task[] = [];


    constructor(fields: Partial<Project>) {
        if (fields) {
            Object.assign(this, fields);
        }
    }

    public toJSON(): ProjectJSON {
        return {
            id: this.id,
            name: this.name,
            description: this.description,
            status: this.status,
            session_time: this.sessionTime,
            created_at: moment(this.createdAt).format('MM/DD/YYYY HH:mm:ss'),
            updated_at: moment(this.updatedAt).format('MM/DD/YYYY HH:mm:ss'),
        };
    }

}

export { Project, ProjectJSON };
