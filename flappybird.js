var flappybird = {};

flappybird.Pipe = Class.extend({

    width: 72,
    height: 180,

    speed: Math.PI + Math.random(),

    order: 0,

    init: function (stage, placement, x, h) {
        this.stage = stage;
        this.placement = placement;
        this.height = h;
        this.x = x || 0;
        this.y = 0;

        if (this.placement == flappybird.BOTTOM) {
            this.y = stage.height - this.height;
        }

        this.img = new Image();
        this.img.src = 'assets/pipe.png';

    },

    update: function () {
        this.x -= this.speed;
    },

    draw: function () {
        var context = this.stage.context,
            pattern = context.createPattern(this.img, "repeat");

        context.fillStyle = pattern;

        // save the current position of canvas
        context.save();

        var yAddition = 0;

        if (this.placement == flappybird.BOTTOM) {
            yAddition = 20;
        }

        context.translate(
            this.x + 4,
            this.y + yAddition
        );

        context.fillRect(0, 0, this.width - 8, this.height - 20);

        context.fillStyle = "#6e217d";

        if (this.placement == flappybird.BOTTOM) {
            context.translate(0, -this.height);
        }

        context.fillRect(-4, this.height - 20, this.width, 20);

        // restore canvas position
        context.restore();


    }
});

flappybird.Bird = Class.extend({

    width: 35,
    height: 30,

    x: 100,
    y: 200,

    states: {
        FLY: 0,
        RISE: 1,
        FALL: 2
    },

    vertSpeed: 0,
    flapState: 0,
    defaultRotation: 0.8,
    minRotation: 0.1,

    init: function (stage) {
        this.stage = stage;
        this.stage.canvas.addEventListener('mousedown', this.flap.bind(this));
        this.stage.canvas.addEventListener('keydown', this.flap.bind(this));

        this.img = new Image();
        this.img.src = 'bird-2.png';

        this.flapState = 0;
        this.rotation = this.defaultRotation;
        this.state = this.states.FLY;

    },

    update: function () {

        if (this.stage.position % 5 == 0) {
            if (++this.flapState == 4) {
                this.flapState = 0
            }
        }

        if (this.stage.state == this.stage.states.GAME_OVER) {
            this.vertSpeed = 10;
            this.rotation += 0.3;
        }

        this.y += this.vertSpeed;

        this.vertSpeed += 0.6;

        if (this.state == this.states.RISE) {
            if (this.rotation >= this.minRotation) {
                this.rotation -= 0.4;
            }

            if (this.flapStartPosition + 10 < this.stage.position) {
                this.state = this.states.FALL;
            }
        }

        if (this.state == this.states.FALL) {
            if (this.flapStartPosition + 5 < this.stage.position) {
                this.state = this.states.FLY;
            }
        }

        if (this.state == this.states.FLY && this.rotation < this.defaultRotation) {
            this.rotation += 0.04;
        }

    },

    draw: function () {

        this.stage.context.save();

        this.stage.context.translate(this.x, this.y);

        this.stage.context.rotate(this.rotation);
        this.stage.context.translate(-(this.x), -(this.y));

        var angle = 0; //Math.PI - 3;
        this.stage.context.setTransform(1, 0, angle, 1, 0, 0);

        this.stage.context.drawImage(
            this.img,
            this.flapState * this.width,
            0,
            this.width,
            this.height,
            this.x,
            this.y,
            this.width,
            this.height
        );

        this.stage.context.restore();
    },

    flap: function () {
        if (this.stage.state != this.stage.states.GAME_OVER) {
            this.vertSpeed = -7;
            this.flapStartPosition = this.stage.position;
            this.state = this.states.RISE;
        }
    },

    reset: function () {
        this.x = 100;
        this.y = this.stage.height / 2;
        this.rotation = this.defaultRotation;
        this.vertSpeed = 0;
    }

});

flappybird.TOP = 0;
flappybird.BOTTOM = 1;

flappybird.Ground = Class.extend({
    width: 780,
    height: 253,

    x: 0,
    y: 0,

    init: function (stage) {
        this.stage = stage;
        this.img = new Image();
        this.img.src = 'assets/ground.png';
        this.y = stage.height - this.height;
    },

    update: function () {

        if (Math.abs(this.x) > this.width) {
            this.x = 0;
        }

        this.x -= 3;

    },

    draw: function () {
        var context = this.stage.context;
        context.drawImage(this.img, this.x, this.y);
        context.drawImage(this.img, this.width - Math.abs(this.x), this.y);
    }

});

flappybird.Cloud = Class.extend({

    width: 108,
    height: 63,

    init: function (stage, x, y, speed) {
        this.stage = stage;
        this.img = new Image();
        this.img.src = 'assets/cloud.png';
        this.x = x;
        this.y = y;
        this.speed = speed;
    },

    update: function () {

        if (this.x > this.stage.width) {
            this.x = -this.width;
        }

        this.x += this.speed;
    },

    draw: function () {
        this.stage.context.drawImage(this.img, this.x, this.y);
    }

});

flappybird.ScoreBoard = Class.extend({

    init: function (stage) {
        this.stage = stage;
    },

    update: function () {},

    draw: function () {
        var scoreText = "Score: " + this.stage.score;
        this.stage.context.textAlign = "left";
        this.stage.context.font = "16px Helvetica";
        this.stage.context.fillStyle = "#000";
        this.stage.context.fillText(scoreText, 12, 25);
    }

});


flappybird.Game = Class.extend({

    width: 800,
    height: 500,

    position: 0,
    score: 0,

    pipeCreationRate: 100,
    pipesHorizontalSpacing: 240,
    pipesVerticalSpacing: 180,

    states: {
        WAIT: 0,
        PLAYING: 1,
        GAME_OVER: 2
    },

    init: function (options) {
        this.canvas = options.canvas;
        this.context = this.canvas.getContext("2d");
        this.bird = new flappybird.Bird(this);
        this.ground = new flappybird.Ground(this);
        this.scoreboard = new flappybird.ScoreBoard(this);
        this.clouds = [
            new flappybird.Cloud(this, 100, 30, 0.1),
            new flappybird.Cloud(this, 300, 60, 0.4),
            new flappybird.Cloud(this, 500, 20, 0.4),
            new flappybird.Cloud(this, 700, 30, 0.1),
        ];
        this.pipes = [];
        this.passedPipes = [];
        this.lastPipe = null;
        this.state = this.states.WAIT;
        this.canvas.addEventListener("click", this.onclick.bind(this));
        this.canvas.addEventListener("mouseup", this.onclick.bind(this), { once: true });
    },

    createPipe: function () {
        if (!this.lastPipe || this.lastPipe.x < (this.width - this.pipesHorizontalSpacing)) {

            var positionX = this.width,
                pipeTop,
                pipeBottom,
                hTop,
                hBottom,
                order;

            hTop = parseInt(Math.random() * (this.height / 2)) + 40;
            hBottom = this.height - this.pipesVerticalSpacing - hTop;


            pipeTop = new flappybird.Pipe(this, flappybird.TOP, positionX, hTop);
            pipeBottom = new flappybird.Pipe(this, flappybird.BOTTOM, positionX, hBottom);

            order = this.pipes.length + 1;

            pipeTop.order = pipeBottom.order = order;

            this.pipes.push(pipeTop);
            this.pipes.push(pipeBottom);

            this.lastPipe = pipeBottom;
        }
    },

    handleCollision: function () {

        if (this.bird.y < -100 || this.bird.y > this.height + 100) {
            this.state = this.states.GAME_OVER;
        }

        for (var i in this.pipes) {
            var pipe = this.pipes[i];

            var collides = this.bird.x > pipe.x - (pipe.width/2)
                        && this.bird.x < pipe.x + pipe.width
                        && this.bird.y > pipe.y
                        && this.bird.y < pipe.y + pipe.height;

            if (collides) {
                this.state = this.states.GAME_OVER;
            }
        }
    },

    updateScore: function () {
        if (this.state == this.states.PLAYING) {
            for (var i in this.pipes) {
                var pipe = this.pipes[i];
                if (this.bird.x > pipe.x + pipe.width) {
                    if (this.passedPipes.indexOf(pipe.order) == -1) {
                        this.passedPipes.push(pipe.order);
                        this.score++;
                    }
                }
            }
        }
    },

    showGameOverScreen: function () {
        this.context.fillStyle = "#000";
        this.context.textAlign = "center";
        this.context.font = "bold 30px helvetica";
        this.context.fillText("GAME OVER but it's ok", 400, 240);
        this.context.fillText("SCORE " + this.score, 400, 280);
    },

    update: function () {

        this.position += 1;

        this.handleCollision();

        this.updateScore();

        this.ground.update();

        this.bird.update();

        this.scoreboard.update();

        this.createPipe();

        for (var cloud in this.clouds) {
            this.clouds[cloud].update();
        }

        for (var pipe in this.pipes) {
            this.pipes[pipe].update();
        }

    },

    draw: function () {

        this.clear();

        this.ground.draw();

        for (var cloud in this.clouds) {
            this.clouds[cloud].draw();
        }

        for (var pipe in this.pipes) {
            this.pipes[pipe].draw();
        }

        this.bird.draw();

        this.scoreboard.draw();

        if (this.state == this.states.GAME_OVER) {
            this.showGameOverScreen();
        }

    },

    clear: function () {
        this.context.fillStyle = "#d9ffff";
        this.context.fillRect(0, 0, this.width, this.height)
    },

    onclick: function () {
        if (this.state == this.states.WAIT) {
            this.state = this.states.PLAYING;
        }

        if (this.state == this.states.GAME_OVER) {
            this.reset();
        }
    },

    reset: function () {
        this.state = this.states.WAIT;
        this.bird.reset();
        this.score = 0;
        this.position = 0;
        this.pipes = [];
        this.lastPipe = null;
    },

    loop: function () {
        this.update();
        this.draw();
        
        // TODO: calculate a time delta in order to set a fixed fps
        (window.requestAnimationFrame || function (callback) {
            setTimeout(callback, 1000 / 60)
        })(this.loop.bind(this));
    }

});
