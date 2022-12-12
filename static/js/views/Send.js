import AbstractView from "./AbstractView.js";

export default class extends AbstractView {
    constructor() {
        super();
        this.setTitle("Send");
    }

    async getHtml() {
        return `
            <section class="center"> 
            <section class="title">
                <h2> New Delivery </h2>
            </section>
            
            <section class="selections"> 
                <a href="/req_robot" class="btn Introduce">Call robot</a>
                <a href="/scan_barcode" class="btn Introduce">Scan barcode</a>
                <a href="/start_mission" class="btn Move">Start mission</a>
            </section>
        `;
    }
}