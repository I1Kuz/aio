import { Application, Graphics } from 'pixi.js';

(async () =>
{
    // Create a new application
    const app = new Application();

    // Initialize the application
    await app.init({  
        resizeTo: window, 
        antialias: true,
        background: 0x111111
    });

    app.canvas.style.position = 'absolute';
    // Append the application canvas to the document body
    document.body.appendChild(app.canvas)

    const rectangle = new Graphics()
        .rect(200, 200, 200, 200)  
        .fill({       
        color: 0xffea00,
        alpha: 0.8
    })
    // .stroke({
    //     width:8,
    //     color: 0x00ff00
    // })
    app.stage.addChild(rectangle);

    const line = new Graphics()
    .moveTo(100, 700)
    .lineTo(0, 400)
    .stroke({
        color: 0x5500ff
    });
    app.stage.addChild(line);
})();
