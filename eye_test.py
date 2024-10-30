from fasthtml.common import *

app, rt = fast_app()

@rt("/")
def get():
    return Titled("Eye Test",
        # Controls
        Div(cls="controls")(
            Label("Speed:", 
                Input(type="range", min="1", max="20", value="5", id="speed", name="speed",
                      hx_trigger="input", hx_post="/update-speed", hx_target="#dot-script")),
            Label("Size:", 
                Input(type="range", min="5", max="50", value="20", id="size", name="size",
                      hx_trigger="input", hx_post="/update-size", hx_target="#dot-script"))
        ),
        
        # Dot container - removed fixed height and added full width
        Div(id="dot-container", style="position: relative; height: 300px; width: 100%; margin: 20px 0;")(
            Div(id="dot")
        ),
        
        # Animation script
        Div(id="dot-script")(
            Script("""
                let dot = me('#dot');
                let speed = parseInt(me('#speed').value) || 5;
                let size = parseInt(me('#size').value) || 20;
                let position = 0;
                let direction = 1;

                // Set initial dot style
                function updateDotStyle() {
                    dot.styles({
                        'position': 'absolute',
                        'width': size + 'px',
                        'height': size + 'px',
                        'background': 'black',
                        'border-radius': '50%',
                        'left': position + 'px',
                        'top': '50%',
                        'transform': 'translateY(-50%)'
                    });
                }

                updateDotStyle();

                // Animation function
                function animate() {
                    let container = me('#dot-container');
                    let maxX = container.offsetWidth - size;
                    
                    position += direction * speed;
                    
                    if (position >= maxX) {
                        position = maxX;
                        direction = -1;
                    } else if (position <= 0) {
                        position = 0;
                        direction = 1;
                    }
                    
                    dot.styles({'left': position + 'px'});
                    requestAnimationFrame(animate);
                }

                animate();

                // Handle window resize
                window.addEventListener('resize', function() {
                    let container = me('#dot-container');
                    let maxX = container.offsetWidth - size;
                    if (position > maxX) {
                        position = maxX;
                    }
                });
            """)
        ),
        
        # Styles - added container styles
        Style("""
            .controls {
                display: flex;
                gap: 20px;
                margin: 20px 0;
            }
            .controls label {
                display: flex;
                align-items: center;
                gap: 10px;
            }
            #dot-container {
                background: #f5f5f5;
                border-radius: 8px;
                overflow: hidden;
            }
            main.container {
                max-width: 100% !important;
                padding: 0 1rem;
            }
        """)
    )

@rt("/update-speed")
async def post(request):
    form = await request.form()
    speed = form.get("speed", "5")
    return Script(f"""
        speed = parseInt({speed});
        console.log('Speed updated to:', speed);
    """)

@rt("/update-size")
async def post(request):
    form = await request.form()
    size = form.get("size", "20")
    return Script(f"""
        size = parseInt({size});
        updateDotStyle();
        console.log('Size updated to:', size);
    """)

serve()
