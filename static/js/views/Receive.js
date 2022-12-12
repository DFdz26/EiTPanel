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
                <h2> Mission Control </h2>
            </section>

            <p>
                After pickup choose next goal
            </p>
            
            <section class="selections"> 
                <a href="/continue_mission" class="btn Introduce">Next Station</a>
                <a href="/continue_mission" class="btn Introduce">Warehouse</a>
            </section>
        `;
    }
}