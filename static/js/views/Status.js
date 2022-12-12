import AbstractView from "./AbstractView.js";

export default class extends AbstractView {
    constructor() {
        super();
        this.setTitle("Status");
    }

    async getHtml() {
        return `
            <section class="center"> 
                <section class="title">
                    <h2> Mission status </h2>
                </section>
                <p>
                    Possibility to display mission status and current robot's position in the future
                </p>
                <p>
                    <a href="/" class="btn Introduce" data-link>New mission</a>
                </p>
            </section>
        `;
    }
}