export default class ServiceStatus {
    private code: number;
    private message: string;
    private data: any = {};

    constructor(code: number, message: string) {
        this.code = code;
        this.message = message;
    }
}
