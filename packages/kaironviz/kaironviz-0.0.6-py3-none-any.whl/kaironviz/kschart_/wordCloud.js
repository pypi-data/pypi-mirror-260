class WordCloud {
    constructor({
        parent = document.body,
        height = 450,
        width = 700,
        fontFamily = 'Arial',
        colorMode = true,
        maxFontSize = 60,
        minFontSize = 10,
        maxItem = 200,
        backgroundColor = 'transparent',
    }) {
        this.parentElement = parent ?? document.body;
        this.height = height;
        this.width = width;
        this.fontFamily = fontFamily;
        this.colorMode = colorMode;
        this.maxFontSize = maxFontSize;
        this.minFontSize = minFontSize;
        this.maxItem = maxItem;
        this.canvas = document.createElement('canvas');
        this.canvas.height = height;
        this.canvas.width = width;
        this.canvas.style.backgroundColor = backgroundColor;
        this.parentElement.appendChild(this.canvas);
        this.ctx = this.canvas.getContext('2d');
        this.wordRects = [];
        this.mouse = { x: 0, y: 0 };
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
            this.mouse.x = e.clientX - rect.left;
            this.mouse.y = e.clientY - rect.top;
            const xpos = rect.left - pRect.left + this.mouse.x;
            const ypos = rect.top - pRect.top + this.mouse.y;
            const mouseRect = { x: this.mouse.x, y: this.mouse.y, width: 1, height: 1 };
            for (let word of this.wordList) {
                if (word.dontPlace) continue;
                if (this.intersect(word.rect, mouseRect)) {
                    this.overlay.innerHTML = `${word.text}<br/>${word.count} &nbsp; times`;
                    this.overlay.style.top = `${ypos + 10}px`;
                    this.overlay.style.left = `${xpos + 10}px`;
                    this.overlay.style.display = 'block';
                    return;
                }
            }
            this.overlay.style.display = 'none';
        });
    }

    generatePackedLayout(words) {
        let sortedWords = words.slice().sort((a, b) => b.count - a.count);
        if (sortedWords.length > this.maxItem) sortedWords = sortedWords.slice(0, this.maxItem);
        const maxCount = sortedWords[0].count;
        const minCount = sortedWords[sortedWords.length - 1].count;
        const maxFontSize = this.maxFontSize;
        const minFontSize = this.minFontSize;
        const fontScale = (maxFontSize - minFontSize) / (maxCount - minCount);

        sortedWords = sortedWords.map((word) => {
            const fontSize = Math.floor(minFontSize + fontScale * (word.count - minCount));
            return { text: word.text, size: fontSize, count: word.count };
        });

        sortedWords.forEach((word) => {
            this.ctx.font = `${word.size}px ${this.fontFamily}`;
            const w = this.ctx.measureText(word.text).width + 5;
            const orientation =
                Math.random() < 0.2 && w < (this.canvas.height * 2) / 3 ? 'vertical' : 'horizontal';
            const width = orientation === 'vertical' ? word.size : w;
            const height = orientation === 'horizontal' ? word.size : w;

            const position = this.findEmptyPosition(width, height);
            if (position) {
                word.x = position.x;
                word.y = position.y + 4;
                word.orientation = orientation;
                word.rect = { x: position.x, y: position.y, width, height };
                this.wordRects.push(word.rect);
            } else {
                word.dontPlace = true;
            }
        });
        this.wordList = sortedWords;
    }

    findEmptyPosition(width, height) {
        const maxAttempts = 250;
        const gridSize = 2;

        for (let attempt = 0; attempt < maxAttempts; attempt++) {
            const x = this.getRandomGridPosition(this.canvas.width - width, gridSize);
            const y = this.getRandomGridPosition(this.canvas.height - height, gridSize);

            const isPositionEmpty = !this.wordRects.some((rect) =>
                this.intersect({ x, y, width, height }, rect)
            );

            if (isPositionEmpty) {
                return { x, y };
            }
        }

        return null;
    }

    getRandomGridPosition(max, gridSize, padding = 10) {
        return Math.floor(Math.random() * ((max - padding) / gridSize)) * gridSize + padding;
    }

    intersect(rect1, rect2) {
        return (
            rect1.x < rect2.x + rect2.width &&
            rect1.x + rect1.width > rect2.x &&
            rect1.y < rect2.y + rect2.height &&
            rect1.y + rect1.height > rect2.y
        );
    }

    plot({ data }) {
        this.generatePackedLayout(data);
        this.draw();
    }
    draw() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        const colors = [
            'scarlet',
            'green',
            'dodgerblue',
            'black',
            'purple',
            'tomato',
            'deeppink',
            'brown',
            'lightSeaGreen',
            'gray',
        ];
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        this.ctx.font = this.font;

        this.wordList.forEach((word) => {
            if (word.dontPlace) return;
            if (this.colorMode) {
                const color = colors[Math.floor(Math.random() * colors.length)];
                this.ctx.fillStyle = color;
            }
            this.ctx.save();
            this.ctx.translate(word.x, word.y);

            this.ctx.font = `${word.size}px ${this.font}`;
            if (word.orientation === 'vertical') {
                this.ctx.rotate(Math.PI / 2);
                this.ctx.textBaseline = 'alphabetic';
            } else {
                this.ctx.textBaseline = 'hanging';
            }
            this.ctx.fillText(word.text, 0, 0);

            this.ctx.restore();
        });
    }
}
