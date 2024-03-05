class TreeDiagram {
    constructor({ parent, data, isVertical }) {
        this.container = parent || document.body;
        this.container.attachShadow({ mode: 'open' });
        this.container.shadowRoot.innerHTML = containerContent;
        this.isVertical = isVertical;
        this.data = data;
        this.render();
    }

    render() {
        let container = this.container.shadowRoot.querySelector('#tree');
        container.innerHTML = this.createTree(this.data);
    }

    createTree(data) {
        if (typeof data === 'string' || typeof data === 'number' || typeof data === 'boolean') {
            if (!this.isVertical) return `<li><code><div class='cac'>${data}</div></code></li>`;
            return '<li><code>' + data + '</code></li>';
        } else if (Array.isArray(data)) {
            let html = '';
            for (let i = 0; i < data.length; i++) {
                html += `${this.createTree(data[i])}`;
            }
            return html;
        } else if (typeof data === 'object') {
            let html = '';
            for (let key in data) {
                html += '<li>';
                if (!this.isVertical) html += `<code><div class='cac'>${key}</div></code>`;
                else html += `<code>${key}</code>`;
                html += `<ul>${this.createTree(data[key])}</ul>`;
                html += '</li>';
            }
            return html;
        }
    }
}
