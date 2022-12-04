import AbstractView from "./AbstractView.js";

export default class extends AbstractView {
    constructor() {
        super();
        this.setTitle("Receive");
    }

    async getHtml() {
        return `
            <section class="center"> 
            <section class="title">
                <h2> Load control </h2>
            </section>
            
            <section class="selections"> 
                <a href="#" class="btn Scan">Confirm Pickup</a>
            </section>
        `;
    }
}