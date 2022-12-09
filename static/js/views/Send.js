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
                <h2> MiR control </h2>
            </section>
            
            <section class="selections"> 
                <a href="#" class="btn Introduce">Call robot</a>
                <a href="/scan" class="btn Introduce" data-link>Scan barcode</a>
                <a href="#" class="btn Move">Start mission</a>
            </section>
        `;
    }
}