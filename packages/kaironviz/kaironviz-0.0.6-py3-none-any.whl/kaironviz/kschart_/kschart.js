class KSChart {
    constructor({
        parent = document.body,
        height = 450,
        clientHeight = 0,
        fromprefix = '',
        toprefix = '',
        fromSuffix = '',
        toSuffix = '',
        showToolbar = true,
        nodeWidth = 14,
        verticalSpacing = 30,
        textColor = '#333',
        textScale = 1,
        textFont = 'Arial',
        drawColumnLebels = true,
        drawLabels = true,
        labelDistance = 10,
        colorMode = 1,
        useGradient = true,
    }) {
        this.parent = parent;
        this.height = height;
        this.clientHeight = clientHeight;
        this.elem = document.createElement('div');
        this.elem.classList.add('ks-chart');
        this.elem.style.width = '100%';
        let shouldScroll = clientHeight > 0 && clientHeight < height;
        this.elem.style.height = `${shouldScroll ? clientHeight : height}px`;
        this.shouldScroll = shouldScroll;
        this.parent.appendChild(this.elem);
        this.mouse = {
            x: 0,
            y: 0,
        };
        this.senseMove = true;

        this.fromprefix = fromprefix;
        this.toprefix = toprefix;
        this.fromSuffix = fromSuffix;
        this.toSuffix = toSuffix;
        this.showToolbar = showToolbar;
        this.nodeWidth = nodeWidth;
        this.verticalSpacing = verticalSpacing;
        this.textColor = textColor;
        this.textScale = textScale;
        this.textFont = textFont;
        this.drawColumnLebels = drawColumnLebels;
        this.drawLabels = drawLabels;
        this.labelDistance = labelDistance;
        this.colorMode = colorMode;
        this.useGradient = useGradient;
        this.isFilterChanged = false;
        this.cachedParsedData = null;

        let uid = Math.random().toString(36).substr(2, 9);
        this.uid = uid;
        this.id_ = `ks-chart-${uid}_`;
    }

    randomColor() {
        let h = Math.floor(Math.random() * 360);
        let s = Math.floor(Math.random() * 30) + 40;
        let l = Math.floor(Math.random() * 30) + 50;

        return `hsl(${h}, ${s}%, ${l}%)`;
    }

    randomColorGradient(ctx) {
        let gradient = ctx.createLinearGradient(0, 0, 0, 450);
        gradient.addColorStop(0, this.randomColor());
        gradient.addColorStop(1, this.randomColor());
        return gradient;
    }

    draw() {
        let canvas = this.elem.querySelector('.ks-chart-canvas');

        if (!this.senseMove && this.LastRects) {
            canvas.style.cursor = 'default';

            for (let i = 0; i < this.LastRects.length; i++) {
                let rect = this.LastRects[i];
                //check if a rect is intercepting with mouse
                if (
                    this.mouse.x > rect.x &&
                    this.mouse.x < rect.x + rect.width &&
                    this.mouse.y > rect.y &&
                    this.mouse.y < rect.y + rect.height &&
                    i + 1 !== this.intersectRect
                ) {
                    //changing mose cursor
                    canvas.style.cursor = 'pointer';
                    this.senseMove = true;
                }
            }
            if (!this.senseMove) return;
        }

        let ctx = canvas.getContext('2d');
        let pbbox = this.parent.getBoundingClientRect();
        let width = (canvas.width = pbbox.width);
        canvas.height = this.height;
        let height = canvas.height - 20;

        // Filter the data based on selected headers
        let selectedHeaders = this.showToolbar
            ? this.headers.filter((h) => {
                  let id = `${this.id_}${h}`;
                  let elem = this.elem.querySelector(`#${id}`);
                  return elem.checked;
              })
            : this.headers;

        // Clear the canvas
        ctx.clearRect(0, 0, width, height);

        // Node positions
        let rects = [];
        let links = [];
        let nodeWidth = this.nodeWidth; // Width of the boxes
        let margin = (width * 0.7 - nodeWidth * selectedHeaders.length) / selectedHeaders.length;
        let verticalSpacing = this.verticalSpacing; // Vertical spacing between boxes
        let curveRadius = margin / 3; // Radius of the curved links

        let totalNodeHeight = 0;
        let maxNodeWidth = 0;
        let graphData = this.parse(this.data, selectedHeaders);
        if (!this.type2) {
            for (let i = 0; i < selectedHeaders.length; i++) {
                let col = graphData[i];
                let nodes = col.nodes;
                let colHeight = nodes.length * verticalSpacing;
                if (colHeight > totalNodeHeight) {
                    totalNodeHeight = colHeight;
                    maxNodeWidth = nodeWidth;
                }
            }
            let scale = Math.min(height / totalNodeHeight, 1);
            verticalSpacing *= scale;

            let ColTotalHeights = selectedHeaders.map((v) => 0);
            for (let i = 0; i < graphData.length; i++) {
                let col = graphData[i];
                let nodes = col.nodes;
                for (let j = 0; j < nodes.length; j++) {
                    let node = nodes[j];
                    ColTotalHeights[i] += node.freq * verticalSpacing;
                }
            }

            let maxPlacebleNodes = Math.floor(height / (this.textScale * verticalSpacing));
            let mp_ = 1 / maxPlacebleNodes;

            let maxY = 0;
            let maxYs = [];
            let nodeOffsets = [0];
            for (let i = 0; i < graphData.length; i++) {
                let col = graphData[i];
                let nodes = col.nodes;
                nodeOffsets.push(nodeOffsets[i] + nodes.length);
                let x = margin + i * (maxNodeWidth + margin);
                let y = (height - nodes.length * verticalSpacing) / 2;

                for (let j = 0; j < nodes.length; j++) {
                    let node = nodes[j];
                    let nodeHeight = node.freq * verticalSpacing;
                    let nodeDrawHeight = nodeHeight;
                    let nodeYOff = 0;
                    if (nodeHeight / ColTotalHeights[i] < mp_) {
                        nodeHeight = ColTotalHeights[i] * mp_;
                        nodeDrawHeight = nodeHeight;
                    } else if (nodeHeight * 0.8 > mp_) {
                        nodeDrawHeight = nodeHeight * 0.8;
                        nodeYOff = (nodeHeight - nodeDrawHeight) / 2;
                    }
                    rects.push({
                        x,
                        y: y + nodeYOff,
                        width: maxNodeWidth,
                        height: nodeDrawHeight,
                        node,
                        col: i,
                    });
                    y += nodeHeight + verticalSpacing;
                    maxY = Math.max(maxY, y);
                }
                maxYs.push(maxY);
                maxY = 0;
            }
            //scale rect height to height
            for (let i = 0; i < rects.length; i++) {
                let scl = height / maxYs[rects[i].col];
                let rect = rects[i];
                rect.height *= scl;
                rect.y *= scl;
            }
            for (let i = 0; i < graphData.length - 1; i++) {
                let _links = graphData[i].links;
                let prevNodes = graphData[i].nodes;
                let nextNodes = graphData[i + 1].nodes;
                for (let l of _links) {
                    if (!prevNodes[l.source] || !nextNodes[l.target]) continue;
                    links.push({
                        sourceCol: l.sourceCol,
                        targetCol: l.targetCol,
                        source: nodeOffsets[i] + l.source,
                        target: nodeOffsets[i + 1] + l.target,
                        value: l.value / prevNodes[l.source].freq,
                        tValue: l.value / nextNodes[l.target].freq,
                    });
                }
            }
        } else {
            selectedHeaders = selectedHeaders.sort((a, b) => a - b);
            let nodes = graphData.nodes;
            let links_ = graphData.links;
            maxNodeWidth = nodeWidth;
            let ys = selectedHeaders.map((v) => 20);

            let ColTotalHeights = selectedHeaders.map((v) => 0);
            for (let node of nodes) {
                let colIndex = selectedHeaders.indexOf(node.level);
                ColTotalHeights[colIndex] +=
                    Math.max(node.freqSrc, node.freqDest) * verticalSpacing;
            }
            let maxPlacebleNodes = Math.floor(height / (this.textScale * verticalSpacing));
            let mp_ = 1 / maxPlacebleNodes;

            for (let node of nodes) {
                let colIndex = selectedHeaders.indexOf(node.level);

                let x = margin + colIndex * (maxNodeWidth + margin);

                let nodeHeight = Math.max(node.freqSrc, node.freqDest) * verticalSpacing;
                if (nodeHeight / ColTotalHeights[colIndex] < mp_) {
                    nodeHeight = ColTotalHeights[colIndex] * mp_;
                }
                rects.push({
                    x,
                    y: ys[colIndex],
                    width: maxNodeWidth,
                    height: nodeHeight,
                    node,
                    colIndex,
                });
                ys[colIndex] += nodeHeight + verticalSpacing;
            }

            //scale rect height to height
            for (let i = 0; i < rects.length; i++) {
                let scl = height / ys[rects[i].colIndex];
                let rect = rects[i];
                rect.height *= scl;
                rect.y *= scl;
            }

            let colNodeCounts = ys.map((v) => 0);
            for (let node of nodes) {
                colNodeCounts[selectedHeaders.indexOf(node.level)]++;
            }

            for (let l of links_) {
                links.push({
                    source: l.sorceId,
                    target: l.targetId,
                    value: l.value / Math.max(nodes[l.sorceId].freqSrc, nodes[l.sorceId].freqDest),
                    tValue:
                        l.value / Math.max(nodes[l.targetId].freqSrc, nodes[l.targetId].freqDest),
                });
            }
        }
        this.LastRects = rects;

        let intersectRect = 0;
        canvas.style.cursor = 'default';
        //drawing nodes
        for (let i = 0; i < rects.length; i++) {
            let rect = rects[i];
            let node = rect.node;
            if (!this.type2 || this.colorMode == 0) {
                ctx.fillStyle = this.colorPallet[i % this.colorCount];
            } else {
                let levelIndex = selectedHeaders.indexOf(rect.node.level);
                ctx.fillStyle = this.colorPallet[levelIndex % this.colorCount];
            }
            ctx.fillRect(rect.x, rect.y, rect.width, rect.height);

            if (this.drawLabels && rect.height > 2) {
                ctx.fillStyle = this.textColor;
                ctx.font = `${Math.ceil(11 * this.textScale)}px ${this.textFont}`;

                let text =
                    String(node.name).substring(0, this.trancation) +
                    (String(node.name).length > this.trancation ? '...' : '');
                ctx.fillText(
                    text,
                    rect.x + nodeWidth + this.labelDistance,
                    rect.y + rect.height / 2
                );
            }
            //check if a rect is intercepting with mouse
            if (
                this.mouse.x > rect.x &&
                this.mouse.x < rect.x + rect.width &&
                this.mouse.y > rect.y &&
                this.mouse.y < rect.y + rect.height
            ) {
                rect.intersect = true;
                intersectRect = i + 1;
                this.intersectRect = i + 1;
                //changing mose cursor
                canvas.style.cursor = 'pointer';
            }
        }

        if (this.drawColumnLebels) {
            if (!this.type2) {
                //drawing column names
                for (let i = 0; i < selectedHeaders.length; i++) {
                    let col = graphData[i];
                    let nodes = col.nodes;
                    let x = margin + i * (maxNodeWidth + margin);
                    let y = canvas.height - 2;
                    ctx.fillStyle = this.textColor;
                    ctx.font = `${Math.ceil(14 * this.textScale)}px ${this.textFont}`;

                    ctx.fillText(selectedHeaders[i], x + 4, y - 4);
                }
            } else {
                //drawing column names
                for (let i = 0; i < selectedHeaders.length; i++) {
                    let x = margin + i * (maxNodeWidth + margin);
                    let y = canvas.height - 2;
                    ctx.fillStyle = this.textColor;
                    ctx.font = `${Math.ceil(14 * this.textScale)}px ${this.textFont}`;
                    ctx.fillText(selectedHeaders[i], x + 4, y - 4);
                }
            }
        }
        //drawing ribbon-like links
        ctx.globalAlpha = 0.2; // Set transparency
        ctx.fillStyle = this.ribbonStyle; // Fill color for links

        let interAlpha = 0.7;
        let dones = rects.map((r) => 0);
        let tDones = rects.map((r) => 0);
        let resetAlpha = false;

        for (let i = 0; i < links.length; i++) {
            let link = links[i];
            let source = rects[link.source];
            let target = rects[link.target];

            let h1 = source.y + source.height * Math.min(dones[link.source], 1.0);
            let h2 = source.height * Math.min(dones[link.source] + link.value, 1.0);
            let h3 = target.y + target.height * Math.min(tDones[link.target], 1.0);
            let h4 = target.height * Math.min(tDones[link.target] + link.tValue, 1.0);

            const sourceTargetDistance = Math.abs(source.x - target.x);
            //bending the curve if the source and target are very far
            if (sourceTargetDistance > 200) {
                curveRadius = sourceTargetDistance / 2;
            }
            //bend ing the curve if the source and target are very close
            else if (sourceTargetDistance <= source.width + target.width) {
                curveRadius = margin / 2;
            } else {
                curveRadius = margin / 3;
            }

            if (
                intersectRect > 0 &&
                (link.source === intersectRect - 1 || link.target === intersectRect - 1)
            ) {
                ctx.globalAlpha = interAlpha;
                resetAlpha = true;
            } else {
                resetAlpha = false;
            }
            if (!this.type2 || this.colorMode == 0) {
                ctx.fillStyle = this.colorPallet[link.source % this.colorCount];
            } else {
                let levelIndex = selectedHeaders.indexOf(rects[link.source].node.level);
                ctx.fillStyle = this.colorPallet[levelIndex % this.colorCount];
            }

            ctx.beginPath();
            ctx.moveTo(source.x + source.width, h1);
            ctx.bezierCurveTo(
                source.x + source.width + curveRadius,
                h1,
                target.x - curveRadius,
                h3,
                target.x,
                h3
            );
            ctx.lineTo(target.x, target.y + h4);
            ctx.bezierCurveTo(
                target.x - curveRadius,
                target.y + h4,
                source.x + source.width + curveRadius,
                source.y + h2,
                source.x + source.width,
                source.y + h2
            );
            ctx.closePath();
            ctx.fill();

            if (resetAlpha) ctx.globalAlpha = 0.2;

            dones[link.source] += link.value;
            tDones[link.target] += link.tValue;
        }

        ctx.globalAlpha = 1; // Resetting transparency

        if (intersectRect > 0) {
            let rect = rects[intersectRect - 1];
            let node = rect.node;

            //box around node
            if (!this.type2 || this.colorMode == 0) {
                ctx.fillStyle = this.colorPallet[(intersectRect - 1) % this.colorCount];
            } else {
                let levelIndex = selectedHeaders.indexOf(rect.node.level);
                ctx.fillStyle = this.colorPallet[levelIndex % this.colorCount];
            }
            ctx.fillRect(rect.x - 2, rect.y - 2, rect.width + 4, rect.height + 4);

            let text = `${node.name} (${node.freq})`;
            let textWidth = ctx.measureText(text).width;
            let textHeight = 20;
            let x = rect.x + rect.width / 2 - textWidth / 2;
            let y = rect.y + rect.height / 2 - textHeight / 2;
            ctx.fillStyle = '#0008';
            ctx.fillRect(this.mouse.x + 10, this.mouse.y + 10, textWidth + 10, textHeight + 10);
            ctx.fillStyle = '#fff';
            ctx.fillText(text, this.mouse.x + 10 + 5, this.mouse.y + 10 + textHeight);

            //writing summary at the right side of canvas
            //how many links came from and can to this node and to and from where

            let from = links
                .filter((l) => l.target === intersectRect - 1)
                .map((l) => {
                    let source = rects[l.source];
                    return {
                        name: source.node.name,
                        value: l.value,
                        count: l.value * source.node.freq,
                    };
                });
            let to = links
                .filter((l) => l.source === intersectRect - 1)
                .map((l) => {
                    let target = rects[l.target];
                    return {
                        name: target.node.name,
                        value: l.tValue,
                        count: l.tValue * target.node.freq,
                    };
                });

            let fromText = from
                .map(
                    (f) =>
                        `${this.fromprefix} ${String(f.name).substring(0, this.trancation)} : ${
                            f.count
                        } (${Number(f.value * 100).toFixed(2)}%) ${this.fromSuffix}`
                )
                .join('\n');
            let toText = to
                .map(
                    (f) =>
                        `${this.toprefix} ${String(f.name).substring(0, this.trancation)} : ${
                            f.count
                        } (${Number(f.value * 100).toFixed(2)}%) ${this.toSuffix}`
                )
                .join('\n');

            //split fromText into lines
            let fromTextLines = fromText.split('\n');
            fromTextLines.unshift('From');
            let toTextLines = toText.split('\n');
            toTextLines.unshift('To');

            let maxTextWidth = Math.max(
                ...fromTextLines.map((t) => ctx.measureText(t).width),
                ...toTextLines.map((t) => ctx.measureText(t).width)
            );
            let maxTextHeight = Math.max(
                ...fromTextLines.map((t) => 20),
                ...toTextLines.map((t) => 20)
            );

            let fromTextX = canvas.width - maxTextWidth - 20;
            //scroll offset with respect to parent
            let cnv = ctx.canvas;
            let scrollOffset =
                cnv.parentElement.getBoundingClientRect().top - cnv.getBoundingClientRect().top;
            let fromTextY = 20 + scrollOffset;

            let toTextX = canvas.width - maxTextWidth - 20;
            let toTextY = fromTextY + maxTextHeight * fromTextLines.length + 20;
            ctx.fillStyle = '#fff8';
            ctx.fillRect(
                fromTextX,
                fromTextY,
                maxTextWidth + 10,
                maxTextHeight * fromTextLines.length + 10
            );
            ctx.fillRect(
                toTextX,
                toTextY,
                maxTextWidth + 10,
                maxTextHeight * toTextLines.length + 10
            );

            ctx.fillStyle = '#333';

            ctx.fillStyle = this.textColor;
            const setFont = (i) => {
                if (i == 0) ctx.font = `bold ${Math.ceil(14 * this.textScale)}px ${this.textFont}`;
                else ctx.font = `${Math.ceil(14 * this.textScale)}px ${this.textFont}`;
            };
            for (let i = 0; i < fromTextLines.length; i++) {
                setFont(i);
                ctx.fillText(fromTextLines[i], fromTextX + 5, fromTextY + 20 + i * 20);
            }
            for (let i = 0; i < toTextLines.length; i++) {
                setFont(i);
                ctx.fillText(toTextLines[i], toTextX + 5, toTextY + 20 + i * 20);
            }
        }
    }

    render({ legend, legendStyle }) {
        let template = `
<style>
.ks-toolbar {
display: flex;
justify-content: start;
align-items: center;
padding: 10px;
}
.ks-search-input::-webkit-calendar-picker-indicator {
display: none;
}

.ks-select-btn {
border: 1px solid #aaa;
border-radius: 0.5rem;
padding: 1.32rem;
margin: 1rem;
flex: 1;
background-color: transparent;
display: flex;
justify-content: center;
align-items: center;
}

.ks-select-btn:hover {
background-color: #4442;
}

.ks-filter-input {
border: 1px solid #aaa;
border-radius: 0.5rem;
padding: .25rem;
margin: 1rem;
flex: 1;
position:relative;
}
.ks-apply-filter-btn {
position:absolute;
right: 4px;
bottom:4px;
border: 1px solid #aaa;
border-radius: 0.5rem;
padding: .5rem;
flex: 1;
background-color: transparent;
}

.ks-apply-filter-btn:hover {
background-color: #4442;
}

.ks-chip,
.ks-search-input {
font-family: sans-serif;
font-size: .85rem;
margin: .25rem;
padding: 0.5rem;
border-radius: 1rem;
color: ${this.textColor}
}

.ks-chip > span {
    padding-right: 0.5rem;
    padding-left: 0.5rem;
}
.ks-chip > span:last-child {
    padding-right: 0.2rem;
    color: #f84;
    font-weight: bold;
    cursor: pointer;
}


.ks-chip {
background-color: #ddd;
display: inline-block;
}

.
</style>`;
        if (this.showToolbar)
            template += `<div class="ks-toolbar">
<div class="ks-chart-levels" style="position: relative">
<div style="position: relative; display: inline-block;">
<button class="ks-select-btn" onClick="let ne = this.nextElementSibling; ne.style.display = ne.style.display === 'none'? 'block' : 'none'; " ><span>Select Levels</span> &nbsp; <svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 512 512" height="1rem" width="1rem" xmlns="http://www.w3.org/2000/svg"><path fill="none" stroke-linecap="round" stroke-linejoin="round" stroke-width="48" d="M112 268l144 144 144-144M256 392V100"></path></svg></button>
<div style="display: none; position: absolute; background-color: #f9f9f9; min-width: 200px;  box-shadow: 0px 8px 16px 2px rgba(0,0,0,0.2); z-index: 1;">
${this.headers
    .map((h) => {
        return `<label style="display: block; padding: 4px;">
<input type="checkbox" id="${this.id_}${h}" style="margin-right: 5px;">${h}
</label>`;
    })
    .join('')}
</div>
</div>
</div>
<fieldset class="ks-filter-input">
<legend>Filter Data</legend>
<div style="display: inline;" class="ks-filter-chips">
<!-- Chips will be displayed here -->
</div>
<input class="ks-search-input" type="text" style="display: inline-block; border:none; outline: none;"
list="ks-s-search-options-${this.uid}" placeholder="filter by..." onkeydown="
(function (event) {
function createChip(chipContainer, text) {
    const chip = document.createElement('div');
    const chipText = document.createElement('span');
    const chipClose = document.createElement('span');
    chipText.textContent = text;
    chipClose.textContent = 'x';
    chip.appendChild(chipText);
    chip.appendChild(chipClose);
    chipClose.classList.add('ks-chip-close');
    chipClose.addEventListener('click', function () {
    chipContainer.removeChild(chip);
});
chip.classList.add('ks-chip');

chipContainer.appendChild(chip);
}
if (event.key === 'Enter' && this.value.trim() !== '') {
    createChip(this.previousElementSibling, this.value.trim());
    this.value = '';
}
}).call(this, event)

" />
<button class="ks-apply-filter-btn">apply</button>
<datalist id="ks-s-search-options-${this.uid}" class="ks-search-options-list">
${this.filters.map((f) => `<option value="${f}"></option>`).join('')}
<!-- Add more options as needed -->
</datalist>
</fieldset>
</div>`;
        template += `
<h2 style="${legendStyle}">${legend}</h2>
<div style="position: relative; width: 100%; height: 100%; ${
            this.shouldScroll ? 'overflow-y: auto;' : ''
        } overflow-x: hidden;  box-sizing: border-box;">
<canvas class="ks-chart-canvas" script="width: 100%; height: ${
            this.height
        }; box-sizing: border-box;"></canvas>
</div>
`;
        this.elem.innerHTML = template;
        let canvas = this.elem.querySelector('.ks-chart-canvas');
        canvas.style.height = `${this.height}px`;
        this.colorPallet = [];
        this.colorCount = 30;
        let ctx = canvas.getContext('2d');
        this.ribbonStyle = this.randomColorGradient(ctx);
        for (let i = 0; i < this.colorCount; i++) {
            if (this.useGradient) this.colorPallet.push(this.randomColorGradient(ctx));
            else this.colorPallet.push(this.randomColor());
        }
        if (this.showToolbar) {
            this.headers.forEach((h) => {
                let id = `${this.id_}${h}`;
                let elem = this.elem.querySelector(`#${id}`);
                elem.checked = true;
                elem.addEventListener('change', (e) => {
                    this.isFilterChanged = true;
                    this.draw();
                });
                this.elem.querySelector('.ks-apply-filter-btn').addEventListener('click', (e) => {
                    this.isFilterChanged = true;
                    this.draw();
                });
            });
        }
        let inputBox = this.elem.querySelector('.ks-search-input');
        inputBox.addEventListener('input', (e) => {
            if (this.filters.includes(e.target.value)) {
                let chipContainer = inputBox.previousElementSibling;
                const chip = document.createElement('div');
                const chipText = document.createElement('span');
                const chipClose = document.createElement('span');
                chipText.textContent = e.target.value;
                chipClose.textContent = 'x';
                chip.appendChild(chipText);
                chip.appendChild(chipClose);
                chipClose.classList.add('ks-chip-close');
                chipClose.addEventListener('click', () => {
                    this.isFilterChanged = true;
                    chipContainer.removeChild(chip);
                });
                chip.classList.add('ks-chip');
                chipContainer.appendChild(chip);
                e.target.value = '';
                this.isFilterChanged = true;
                this.draw();
            }
        });

        canvas.addEventListener('mousemove', (e) => {
            this.mouse = {
                x: e.offsetX,
                y: e.offsetY,
            };
            this.draw();
        });

        canvas.addEventListener('click', (e) => {
            this.mouse = {
                x: e.offsetX,
                y: e.offsetY,
            };
            this.draw();
            this.senseMove = !this.senseMove;
        });

        this.draw();
    }

    plot({
        data,
        headers,
        legend = 'sanky chart example',
        legendStyle = 'text-align: center; font: 28px Arial',
        trancation = 15,
    }) {
        this.type2 = false;
        if (!headers) headers = [...new Set(...data.map((d) => Object.keys(d)))];

        this.headers = headers;
        this.data = data;
        this.filters = [];
        //add every unique value of each column as a filter ie: '[header]:[value]'
        for (let h of headers) {
            let uniqueVals = [...new Set(data.map((d) => d[h]))];
            for (let v of uniqueVals) {
                this.filters.push(`${h}:${v}`);
            }
        }

        this.trancation = trancation;
        this.render({ legend, legendStyle });
    }

    plot2({
        data,
        srcName,
        destName,
        srcLevel,
        destLevel,
        legend = 'sanky chart - 2',
        legendStyle = 'text-align: center; font: 28px Arial',
        trancation = 15,
    }) {
        this.type2 = true;
        this.data = data;
        this.headers = [
            ...new Set(data.map((d) => d[srcLevel]).concat(data.map((d) => d[destLevel]))),
        ].sort();
        this.headers = this.headers.filter((h) => h !== null);
        this.headers = [...new Set(this.headers)];
        this.filters = [];
        for (let d of data) {
            for (let k in d) {
                this.filters.push(`${k}:${d[k]}`);
            }
        }
        this.filters = [...new Set(this.filters)];
        this.srcName = srcName;
        this.destName = destName;
        this.srcLevel = srcLevel;
        this.destLevel = destLevel;
        this.trancation = trancation;
        this.render({ legend, legendStyle });
    }

    parse(data, headers) {
        if (this.cachedParsedData && !this.isFilterChanged) {
            return this.cachedParsedData;
        }
        this.isFilterChanged = false;
        let filters = [];
        let filterHeaders = {};
        if (this.showToolbar) {
            let chips = this.elem.querySelector('.ks-filter-chips').children;
            for (let c of chips) {
                let text = c.children[0].textContent.trim();
                let header = text.split(':');

                if (header.length === 2) {
                    filters.push({
                        header: header[0],
                        value: header[1],
                    });
                    if (filterHeaders[header[0]]) {
                        filterHeaders[header[0]].push(header[1]);
                    } else {
                        filterHeaders[header[0]] = [header[1]];
                    }
                } else if (header.length > 2) {
                    filters.push({
                        header: header[0],
                        value: header.slice(1).join(':'),
                    });
                    if (filterHeaders[header[0]]) {
                        filterHeaders[header[0]].push(header.slice(1).join(':'));
                    } else {
                        filterHeaders[header[0]] = [header.slice(1).join(':')];
                    }
                }
            }
            filters = [...new Set(filters)];
        }

        let filteredData = data.filter((d) => {
            let flag = true;
            for (let h in filterHeaders) {
                if (
                    !filterHeaders[h].some((v) => {
                        return d[h] == v;
                    })
                ) {
                    flag = false;
                    break;
                }
            }
            return flag;
        });

        // let newOptions = [];
        // for (let d of filteredData) {
        //     for (let k in d) {
        //         newOptions.push(`${k}:${d[k]}`);
        //     }
        // }
        // newOptions = [...new Set(newOptions)];
        // let options = this.elem.querySelector('.ks-search-options-list');
        // options.innerHTML = newOptions.map((o) => `<option value="${o}"></option>`).join('');

        if (filters.length === 0) filteredData = data;
        this.filteredHeaders = Object.keys(filteredData[0]);

        if (this.type2) {
            let nodeNames = [
                ...new Set(
                    filteredData
                        .map((d) => d[this.srcName])
                        .concat(data.map((d) => d[this.destName]))
                ),
            ];
            let nodes = {};
            for (let name of nodeNames) {
                nodes[name] = {
                    name,
                    level: 0,
                    freqSrc: 0,
                    freqDest: 0,
                };
            }

            for (let d of filteredData) {
                nodes[d[this.srcName]].freqSrc++;
                nodes[d[this.destName]].freqDest++;
                nodes[d[this.srcName]].level = d[this.srcLevel];
                nodes[d[this.destName]].level = d[this.destLevel];
            }

            for (let i in nodes) {
                nodes[i].freq = Math.max(nodes[i].freqSrc, nodes[i].freqDest);
            }

            let finalNodeArray = [];
            for (let n in nodes) {
                if (nodes[n].freq === 0) continue;
                finalNodeArray.push(nodes[n]);
            }
            let links = [];
            for (let d of filteredData) {
                let key = `${d[this.srcName]}-${d[this.destName]}`;
                if (!links[key])
                    links[key] = {
                        sorceId: finalNodeArray.findIndex((n) => n.name === d[this.srcName]),
                        targetId: finalNodeArray.findIndex((n) => n.name === d[this.destName]),
                        source: d[this.srcName],
                        target: d[this.destName],
                        value: 0,
                    };
                links[key].value++;
            }

            let finalLinks = [];
            for (let l in links) {
                finalLinks.push(links[l]);
            }

            const returnData = {
                nodes: finalNodeArray,
                links: finalLinks,
            };
            this.cachedParsedData = returnData;
            return returnData;
        } else {
            let colData = {};
            let freq = [];
            if (filteredData[0].hasOwnProperty('_freq_')) {
                for (let d of filteredData) {
                    freq.push(d._freq_);
                }
            }
            for (let d of filteredData) {
                for (let h of headers) {
                    if (!colData[h]) colData[h] = [];
                    colData[h].push(d[h]);
                }
            }

            let cols = [];
            const nodesArray = [];
            const uniqueValsArray = [];
            for (let i = 0; i < headers.length; i++) {
                let h = headers[i];
                let freqsMap = new Map();

                for (let index = 0; index < colData[h].length; index++) {
                    let value = colData[h][index];
                    if (freq.length === 0) {
                        freqsMap.set(value, (freqsMap.get(value) || 0) + 1);
                    } else {
                        freqsMap.set(value, (freqsMap.get(value) || 0) + freq[index]);
                    }
                }

                let uniqueVals = Array.from(freqsMap.keys());
                let freqs = uniqueVals.map((v) => freqsMap.get(v));

                let nodes = uniqueVals.map((v, i) => {
                    return {
                        name: v,
                        freq: freqs[i],
                        level: i,
                    };
                });
                nodesArray.push(nodes);
                uniqueValsArray.push(uniqueVals);
            }

            for (let i = 0; i < headers.length; i++) {
                const h = headers[i];
                const nodes = nodesArray[i];
                const uniqueVals = uniqueValsArray[i];
                let links = [];
                let reverseLinks = []; // Store reverse links

                if (i < headers.length - 1) {
                    let nextHeader = headers[i + 1];
                    let nextUniqueVals = [...new Set(colData[nextHeader])];
                    for (let j = 0; j < nodes.length; j++) {
                        let node = nodes[j];
                        for (let k = 0; k < nextUniqueVals.length; k++) {
                            let nextNode = nextUniqueVals[k];
                            let count = 0;
                            let reverseCount = 0; // Count for reverse links
                            for (let l = 0; l < filteredData.length; l++) {
                                let d = filteredData[l];
                                if (d[h] === node.name && d[nextHeader] === nextNode) {
                                    if (!d._freq_) {
                                        count++;
                                    } else {
                                        count += d._freq_;
                                    }
                                }
                                if (d[h] === nextNode && d[nextHeader] === node.name) {
                                    if (!d._freq_) {
                                        reverseCount++;
                                    } else {
                                        reverseCount += d._freq_;
                                    }
                                }
                            }
                            if (count > 0) {
                                links.push({
                                    sourceCol: i,
                                    targetCol: i + 1,
                                    source: j,
                                    target: k,
                                    value: count,
                                });
                            }
                            if (reverseCount > 0) {
                                reverseLinks.push({
                                    sourceCol: i,
                                    targetCol: i + 1,
                                    source: k,
                                    target: j,
                                    value: reverseCount,
                                });
                            }
                        }
                    }
                }

                cols.push({
                    nodes,
                    links: links.concat(reverseLinks), // Concatenate reverse links
                });
            }

            this.graphData = cols;
            this.cachedParsedData = cols;
            return cols;
        }
    }
}
