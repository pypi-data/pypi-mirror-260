class DrillChart {
    constructor({
        parent,
        ylabel = 'values',
        legend = 'Drill Chart',
        legendColor = 'black',
        legendFont = 'Bold 20px Arial',
        legendPos = 'bottom', // top, bottom
        legendAlign = 'center', // left, center, right
        navColor = '#046688',
        navFont = '16px Arial',
        navJustify = 'right', // left, center, right
        navPadding = '10px',
        labelScale = 1.2,
        labelColor = 'black',
        resolution = 1.2,
        backgroundColor = 'transparent',
        height = 480,
        maxColumnWidth = 60,
        truncation = 20,
    }) {
        this.parentElement = parent ?? document.body;
        this.navElement = document.createElement('div');
        this.navElement.style.color = navColor;
        this.navElement.style.font = navFont;
        this.navElement.fontWeight = 'bold';
        this.navElement.style.textAlign = navJustify;
        this.navElement.style.padding = navPadding;

        this.parentElement.appendChild(this.navElement);
        this.canvas = document.createElement('canvas');
        this.canvas.style.backgroundColor = backgroundColor;

        this.parentElement.appendChild(this.canvas);
        this.ctx = this.canvas.getContext('2d');
        this.margin = {
            top: 20,
            bottom: 90,
            left: 30,
            right: 30,
        };
        this.resolution = resolution;

        this.dataList = [];
        this.clickBoxes = [];
        this.navigation = [];
        this.currentLabel = '';
        this.ylabel = ylabel ?? 'Value';
        this.legend = legend;
        this.legendColor = legendColor;
        this.legendFont = legendFont.trim();
        this.legendPos = legendPos;
        this.legendAlign = legendAlign;
        this.labelScale = labelScale;
        this.labelColor = labelColor;
        this.minHeight = height;
        this.maxColumnWidth = maxColumnWidth;
        this.truncation = truncation;
        this.mouseData = {
            x: 0,
            y: 0,
            index: -0,
            moving: false,
            moveTarget: null,
        };
        this.calculateBounds();
        let bias = 10 * this.resolution;
        this.canvas.addEventListener('click', (e) => {
            let { left, top } = this.canvas.getBoundingClientRect();
            let x = e.clientX - left;
            let y = e.clientY - top;
            x *= this.resolution;
            y *= this.resolution;
            for (let i = 0; i < this.clickBoxes.length; i++) {
                let { x: bx, y: by, w, h } = this.clickBoxes[i];
                if (x > bx && x < bx + w && y > by - bias && y < by + h + bias) {
                    if (!this.triggerLabels) return;
                    if (this.triggerLabels.length === 0) return;
                    if (this.triggerLabels[i].length < 1) continue;
                    this.navigation.push(this.triggerLabels[i]);
                    this.currentLabel = this.triggerLabels[i];
                    this.plot(this.dataList, this.triggerLabels[i]);
                }
            }
        });

        this.overlay = document.createElement('div');
        this.overlay.style.position = 'absolute';
        this.overlay.style.top = '0';
        this.overlay.style.left = '0';
        this.overlay.style.backgroundColor = 'rgba(0,0,0,0.5)';
        this.overlay.style.zIndex = '1000';
        this.overlay.style.backdropFilter = 'blur(5px)';
        this.overlay.style.color = 'white';
        this.overlay.style.padding = '5px 10px';
        this.overlay.style.borderRadius = '5px';
        this.overlay.style.display = 'none';
        this.parentElement.appendChild(this.overlay);

        this.canvas.addEventListener('mousemove', (e) => {
            const rect = e.target.getBoundingClientRect();
            const pRect = this.parentElement.getBoundingClientRect();
            this.mouse = { x: 0, y: 0 };
            this.mouse.x = e.clientX - rect.left;
            this.mouse.y = e.clientY - rect.top;
            const xpos = rect.left - pRect.left + this.mouse.x;
            const ypos = rect.top - pRect.top + this.mouse.y;
            const mouseRect = { x: this.mouse.x, y: this.mouse.y, width: 1, height: 1 };

            let { left, top } = this.canvas.getBoundingClientRect();
            let x = e.clientX - left;
            let y = e.clientY - top;
            x *= this.resolution;
            y *= this.resolution;
            for (let i = 0; i < this.clickBoxes.length; i++) {
                let { x: bx, y: by, w, h } = this.clickBoxes[i];
                if (x > bx && x < bx + w && y > by - bias && y < by + h + bias) {
                    if (this.currentData.xs.length < 1) continue;
                    this.canvas.style.cursor = 'pointer';
                    this.mouseData.index = i;
                    this.mouseData.x = x;
                    this.mouseData.y = y;
                    this.mouseData.moving = true;
                    this.moveTarget = this.clickBoxes[i];

                    this.yval = this.currentData.ys[i];
                    this.xval = this.currentData.xs[i];
                    this.overlay.innerHTML = `${this.xval}&nbsp;( ${this.yval} )`;
                    let xp = xpos + 10;
                    if (xp + this.overlay.offsetWidth > pRect.width) {
                        xp = pRect.width - this.overlay.offsetWidth - 10;
                    }
                    this.overlay.style.top = `${ypos + 10}px`;
                    this.overlay.style.left = `${xp + 10}px`;
                    this.overlay.style.display = 'block';

                    if (!this.triggerLabels || this.triggerLabels.length < 1)
                        this.canvas.style.cursor = 'default';

                    return;
                }
            }

            this.overlay.style.display = 'none';
            this.canvas.style.cursor = 'default';
            this.mouseData.moving = true;
        });

        window.addEventListener('resize', (e) => {
            console.log(this.dataList, this.currentLabel);
            this.plot(this.dataList, this.currentLabel);
        });
    }

    calculateBounds(data) {
        if (data) {
            let maxXLen = 4;
            let maxYLen = 6;
            let { xs, ys } = data;
            for (let i = 0; i < xs.length; i++) {
                maxXLen = Math.min(Math.max(maxXLen, xs[i].length), this.truncation);
                maxYLen = Math.min(Math.max(maxYLen, ys[i].toString().length), this.truncation);
            }
            this.margin.left = 30 * this.labelScale + maxYLen * 4;
            this.margin.bottom = 80 + maxXLen * 6.4;
            console.log(this.margin.left, this.margin.bottom);
        }
        let pRect = this.parentElement.getBoundingClientRect();
        this.canvas.width = pRect.width * this.resolution;
        this.canvas.style.width = pRect.width + 'px';

        this.canvas.height = this.minHeight * this.resolution;
        this.canvas.style.height = this.minHeight + 'px';

        //this.canvas.height = Math.max(this.minHeight, pRect.height);
        this.bounds = {
            left: this.margin.left,
            right: this.canvas.width - this.margin.right,
            top: this.margin.top,
            bottom: this.canvas.height - this.margin.bottom,
            width: this.canvas.width - (this.margin.left + this.margin.right),
            height: this.canvas.height - (this.margin.top + this.margin.bottom),
        };
    }
    intersect(rect1, rect2) {
        return (
            rect1.x < rect2.x + rect2.width &&
            rect1.x + rect1.width > rect2.x &&
            rect1.y < rect2.y + rect2.height &&
            rect1.y + rect1.height > rect2.y
        );
    }

    draw(data) {
        this.currentData = data;
        this.navElement.innerHTML = '';
        for (let i = 0; i < this.navigation.length; i++) {
            let label = this.navigation[i];
            let span = document.createElement('span');
            span.innerText = `${label} ${this.navigation.length - 1 === i ? '' : ' >'} `;
            span.style.cursor = 'pointer';
            span.style.marginRight = '4px';
            span.addEventListener('click', () => {
                let index = this.navigation.indexOf(label);
                this.navigation = this.navigation.slice(0, index + 1);
                this.plot(this.dataList, label);
            });
            this.navElement.appendChild(span);
        }
        let ctx = this.ctx;
        let canvas = this.canvas;
        let { left, right, width, height, top, bottom } = this.bounds;
        let { xs, ys } = data;

        let yMax = Math.max(...ys);
        let yMin = Math.min(...ys);
        let yNorm = (val) => val / yMax;

        ctx.clearRect(0, 0, canvas.width, canvas.height);

        //drawing legend
        {
            ctx.fillStyle = this.legendColor;
            ctx.font = this.legendFont;
            ctx.textBaseline = 'bottom';
            let legLength = ctx.measureText(this.legend).width;
            let x = 0;
            let y = 0;
            if (this.legendPos === 'top') {
                y = 20;
            } else if (this.legendPos === 'bottom') {
                y = canvas.height - 4;
            }
            if (this.legendAlign === 'left') {
                x = 20;
            } else if (this.legendAlign === 'center') {
                x = (canvas.width - legLength) / 2;
            } else if (this.legendAlign === 'right') {
                x = canvas.width - legLength - 20;
            }
            ctx.fillText(this.legend, x, y);
        }
        //drawing lines
        {
            ctx.lineWidth = 2;
            ctx.beginPath();
            ctx.moveTo(left, bottom);
            ctx.lineTo(right, bottom);
            ctx.stroke();

            ctx.lineWidth = 0.5;

            let yStep = yMax / 4;
            ctx.font = `${12 * this.labelScale}px Arial`;
            ctx.setLineDash([5, 5]);
            for (let i = 0; i < 5; i++) {
                let y = bottom - height * (i / 5);
                let val = yNorm(yStep) * i * yMax;
                ctx.beginPath();
                ctx.moveTo(left - 5, y);
                ctx.lineTo(right, y);
                ctx.stroke();

                ctx.fillText(String(Math.floor(val)), left - 30, y + 5);
            }
            ctx.setLineDash([]);
        }

        let barPadding = 10;
        let barWidth = Math.min(
            (right - left - barPadding * 2 * xs.length) / (xs.length + 1),
            this.maxColumnWidth
        );

        //drawing labels
        ctx.fillStyle = 'black';
        ctx.font = '14px Arial';
        let dx = width / (xs.length + 1);
        for (let i = 0; i < xs.length; i++) {
            let x = left + dx * (i + 1);
            let y = bottom + 10;

            ctx.save();
            ctx.translate(x, y);
            ctx.rotate(Math.PI / 2.4);
            const text =
                xs[i].length > this.truncation
                    ? xs[i].substring(0, this.truncation - 3) + '...'
                    : xs[i];
            ctx.fillText(text, 0, 0);
            ctx.restore();
        }

        //drawing axis labels
        let ltHeight = 16;
        ctx.font = `${ltHeight * this.labelScale}px Arial`;
        ctx.fillStyle = this.labelColor;
        ctx.save();
        ctx.translate(10 * this.labelScale + 4, bottom - height / 2);
        ctx.rotate(-Math.PI / 2);
        ctx.fillText(this.ylabel, 0, 0);
        ctx.restore();
        let tlength = ctx.measureText(data.label).width;
        let xLebelY = canvas.height;
        if (this.legendPos === 'bottom') {
            let fontHeight = this.legendFont.split(' ');
            fontHeight = fontHeight[fontHeight.length - 2];
            fontHeight = fontHeight.substring(0, fontHeight.length - 2);

            xLebelY -= Number(fontHeight) + 16;
        }

        ctx.fillText(data.label, (canvas.width - tlength) / 2, xLebelY);

        //drawing bars
        this.clickBoxes = [];
        let barHeight = height * 0.8;

        let maxTextSize = 0;
        for (let i = 0; i < ys.length; i++) {
            let text = ys[i].toString();
            maxTextSize = Math.max(text.length, maxTextSize);
        }
        let fontSize = barWidth / maxTextSize;
        if (fontSize > 22) fontSize = 22;

        for (let i = 0; i < ys.length; i++) {
            let x = left + dx * (i + 1) - barWidth / 2;
            let y = bottom - barHeight * yNorm(ys[i]);
            let w = barWidth;
            let h = barHeight * yNorm(ys[i]) - 2;

            const grd = ctx.createLinearGradient(0, y, 0, height);
            let color1 = this.colorPalette[data.label ?? ''];
            let c1 = data.xLabels ? data.xLabels[i] ?? '' : '';

            let color2 = c1.length ? this.colorPalette[c1] : color1;

            grd.addColorStop(0, color2);
            grd.addColorStop(1, color1);
            ctx.fillStyle = grd;

            ctx.fillRect(x, y, w, h);

            //text
            let text = ys[i].toString();
            ctx.font = `${fontSize}px Consolus`;
            ctx.fillStyle = 'black';
            let textLength = ctx.measureText(text).width;
            ctx.save();
            ctx.translate(x + (w - textLength) / 2, y - 10);
            ctx.fillText(ys[i], 0, 0);
            ctx.restore();

            this.clickBoxes.push({ x, y, w, h });
        }
    }
    getRandomColor() {
        const hue = Math.floor(Math.random() * 360);
        const saturation = 70 + Math.floor(Math.random() * 30);
        const lightness = 60 + Math.floor(Math.random() * 20);

        return `hsl(${hue}, ${saturation}%, ${lightness}%)`;
    }

    plot(dataList, label) {
        if (this.navigation.length < 1) this.navigation.push(label);
        this.dataList = dataList;
        let data = dataList.filter((d) => d.label === label)[0];
        this.calculateBounds(data);
        this.currentData = data;
        this.draw(data);
        this.triggerLabels = data.xLabels;
        this.currentLabel = label;
    }
    makePlot(dataList, label) {
        this.colorPalette = {
            '': this.getRandomColor(),
        };
        for (let d of dataList) {
            if (!this.colorPalette[d.label]) {
                let color = this.getRandomColor();
                while (Object.values(this.colorPalette).includes(color)) {
                    color = this.getRandomColor();
                }
                this.colorPalette[d.label] = color;
            }
        }
        this.plot(dataList, label);
    }
}
