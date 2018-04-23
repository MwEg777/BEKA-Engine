
# BEKA Engine
A Python-based 2D Game engine, inspired by Unity3D

Example project included.

---	***This game engine is based on Python and OpenGL. It only uses PyGame to load image files as strings, the rest is processed by the BEKA Game Engine.***

# Usage
1/Open GameLauncher.Py

2/Modify "Keeper" to your Game project file name. Eg: if your game file is called MyGame.Py, replace Keeper with MyGame

3/Run GameLauncher.Py


**-Note: PyGame is required to load images. To install it, open a cmd window then type: pip install pygame**


# **Classes**:

● **GameObject**: A base class for all Objects in the scene.
		
		
- Properties and Methods:
	- 
	 - **name**:  *string*
	
			A string that defines GameObject's name.

	 - **position**:  *float[]*
	
			A 3-element float array that determines GameObject's position in World Coordinates.

	 - **scale**:  *float[]*
	
			A 3-element float array that determines GameObject's scale.
			
	 - **angle**:  *float*
	
			A float that determines GameObject's orientation in Euler angles.
	
	 - **smoothDamping**:  *bool*
	
			A bool that determines whether this GameObject uses smooth damping for movement.
			When enabled, it uses smooth damping.
			When disabled, it uses linear movement.
			
  	- **setPos**(positionArray): *function* 
  
		  A function that directly sets the position of the GameObject.
  
		- Parameters: 
  
		  - **positionArray**: A 3-element float array that contains the new position of x, y and z of the GameObject in order.

  	- **setScale**(scaleArray): *function* 
  
		  A function that sets the scale of the GameObject.
  
		- Parameters: 
  
		  - **scaleArray**: A 3-element float array that contains the new scale of x, y and z of the GameObject in order.
		  
  	- **getScale**(): *function* 
  
		  A function that returns the scale array of the GameObject.
  
		- Parameters: None
	
  	- **getPos**(): *function* 
  
		  A function that returns the position array of the GameObject.
  
		- Parameters: None
	
  	- **getAngle**(): *function* 
  
		  A function that returns the rotation angle of the GameObject.
  
		- Parameters: None
	
  	- **loadInitialPosition**(): *function* 
  
		  A function that returns the initial position array that the GameObject was instantiated with.
  
		- Parameters: None

  	- **Instantiate**(positionArray = [0, 0, 0], scaleArray = [1, 1, 1],Angle = 0): *function* 
  
		  A function that creates an instance of the GameObject.
  
		- Parameters: 
  
		  - **positionArray**: A 3-element float array that contains the instantiate position of x, y and z of the GameObject in order.
		  - **scaleArray**: A 3-element float array that contains the initial scale of the GameObject.
		  - **Angle**: A float value that determines the initial rotation of the GameObject.

  	- **move**(TargetArray,StepX,StepY,SmoothDamping = True): *function* 
  
		  A function that moves GameObject to a certain location, using either linear transition or smooth damping.
  
		- Parameters: 
  
		  - **TargetArray**: A 3-element float array that contains the target position of x, y and z of the GameObject in order.
		  - **StepX**: A float value that determines the maximum movement speed in X axis.
		  - **StepY**: A float value that determines the maximum movement speed in Y axis.
		  - **SmoothDamping**: A bool that when enabled, uses smooth damping for GameObject's transition to the new location.

  	- **RotateObject**(TargetAngle,Step): *function* 
  
		  A function that gradually rotates GameObject to a target angle.
  
		- Parameters: 
  
		  - **TargetAngle**: A float value that determines the target angle that the GameObject should reach.
		  - **Step**: A float value that determines the rotation speed.
	  
	
  	- **setName**(Name): *function* 
  
		  A function that sets the name of the GameObject.
  
		- Parameters: 
  
		  - **Name**: A string that contains the new name for the GameObject.
		  
----------------

● **SpriteRenderer**: A class that enables game objects to have a sprite, and renders it.

  - Properties and Methods:
	  -	
  
	  - **flipX**:  *bool* 
  
			Bool that flips sprite in X axis when enabled.
  
	  - **flipY**:  *bool*
  
			Bool that flips sprite in Y axis when enabled.
  
  
	- **FlipX**(): *function*
  
		  A function that changes flipX state.
  
	  - Parameters: None
  
  
	 - **FlipY**(): *function*
  
			A function that changes flipY state.
  
		  - Parameters: None  
  
	- **setColor**(newColor): *function* 
  
		  A function that sets the color of the sprite.
  
		- Parameters: 
  
		  - **newColor**: A 4-element array, carrying value of Red,Green,Blue and Alpha in order. each of the 4 elements vary from 0 to 1.

  
  	- **setDensity**(newDensity): *function* 
  
		  A function that sets the pixel density of the sprite in the scene.
  
		- Parameters: 
  
		  - **newDensity**: A float value that determines the new density of the sprite.
  
  	- **DrawSprite**(TextureCoordX1 = 0, TextureCoordX2 = 0, TextureCoordY1 = 0, TextureCoordY2 = 0, WidthToHeightRatio = 1): *function* 
  
		  A function that draws the sprite in the game window.
  
		- Parameters: 
  
		  - **TextureCoordX1**: A float value that determines the starting X point of the sprite in the selected Image.
		  - **TextureCoordX2**: A float value that determines the end X point of the sprite in the selected Image.
		  - **TextureCoordY1**: A float value that determines the starting Y point of the sprite in the selected Image.
		  - **TextureCoordY2**: A float value that determines the starting Y point of the sprite in the selected Image.
		  - **WidthToHeightRatio**: A float value that is required to show sprites in the way they should be. Calculate it using SpriteMeasurer provided with the BEKA Game Engine. 
  	- **SmoothDamp**(current, target, maxVelocity): *function* 
  
		  A function that makes a smooth transition between a current value and a target value.
  
		- Parameters: 
  
		  - **current**: The current value that you want to make a transition from. Constantly provide the function with this value to retrieve the velocity of transition.
		  - **target**: Target value that you want to reach. Can be either static or dynamic.
		  - **maxVelocity**: A float value that represents the velocity that you don't want your object to exceed, Regardless of its distance to the target value.
		  
----------------

● **Rigidbody**: A class that adds physics simulation to your game object.

  - Properties and Methods:
	  -	
  
	  - **gameObject**:  *GameObject* 
  
			The GameObject to which this Rigidbody class is attached. 
			
	  - **gravityAcceleration**:  *float* 
  
			An integer value that determines the gravity acceleration value for your game. Default is 9.8
			
	  - **gravityScale**:  *float* 
  
			Gravity acceleration factor. Default is 1

	  - **linearDrag**:  *float* 
  
			A value that determines the Rigidbody's linear drag factor. Used for simulating air resistance or friction. Default is 0.5

	  - **angularDrag**:  *float* 
  
			A value that determines the Rigidbody's angular drag factor. Default is 0.01

	  - **mass**:  *float* 
  
			A value that determines the Rigidbody's mass. Default is 1

  	- **setMass**(Mass): *function* 
  
		  A function that sets rigidbody's mass.
  
		- Parameters: 
  
		  - **Mass**: The new mass value for the Rigidbody.

  	- **AddForce**(Force = 1.0, Direction = [1,0]): *function* 
  
		  A function that adds a force to the Rigidbody	using a value and a vector.
  
		- Parameters: 
  
		  - **Force**: The amount of force to be added to the Rigidbody.
		  - **Direction**: A 2-element array containing the direction of the applied force in X and Y axis in order.

  	- **AddForceAtPosition**(Force = 1.0, ForcePoint = [0,0], Direction = [1,0]): *function* 
  
		  A function that adds a force to the Rigidbody	using a value and a vector.
  
		- Parameters: 
  
		  - **Force**: The amount of force to be added to the Rigidbody.
		  - **ForcePoint**: A 2-element array containing the point in which the force should be added, in world coordinates.
		  - **Direction**: A 2-element array containing the direction of the applied force in X and Y axis in order.


  	- **AddTorque**(Force = 1.0): *function* 
  
		  A function that adds a torque to the Rigidbody. Rotates it anti-clockwise.
  
		- Parameters: 
  
		  - **Force**: The amount of force to be added to the Rigidbody as torque.

  	- **simulate**(): *function* 
  
		  The main function that processes and simulates the Rigidbody physics. Constantly call this function every frame or game time instance to get your Rigidbody physics to work.
  
		- Parameters: None
 
----------------

● **GameImages**: A class that enables you to use image files in the game, mostly to use with Sprites.

  - Properties and Methods:
 
	  - **imageNames**:  *string[]* 
  
			An array of string containing the names of the image files you wish to import to your game, followed by extension. Eg: ["Beka.png", "Game.jpg"] 
			
  
	  - **currentImage**:  *int* 
  
			A Read-Only integer value that determines which image is currently in use. 
			
	  - **imageCount**:  *int* 
  
			An integer value that determines the amount of image files to load by the game engine.

  	- **curImage**(CurrentImage = 1): *function* 
  
		  A function that sets the current image file in use.
  
		- Parameters: 
  
		  - **CurrentImage**: An integer value that is used to select an image to use.

  	- **getImageCount**(): *function* 
  
		  A function that returns the amount of images that are loaded by the game engine.


----------------

● **UI**: A base class for UI Elements, such as Buttons and Texts.

  - Properties and Methods:
 
	  - **gameObject**:  *GameObject* 
  
			The GameObject that holds this UI Element. 
			
  
	  - **spriteRenderer**:  *SpriteRenderer* 
  
			The SpriteRenderer attached to this UI Element, Responsible for rendering it. 
			
	  - **type**:  *string* 
  
			A string containing the UI Element's type, can be "button" or "char".


	  - **Hovering**:  *bool* 
  
			A bool that determines whether mouse pointer is hovering over the button.

	  - **normalColor**:  *int[]* 
  
			A 4-element array containing a button's normal color, while it's neither hovered over nor pressed.


	  - **hoverColor**:  *int[]* 
  
			A 4-element array containing a button's color while it's hovered over.


	  - **pressedColor**:  *int[]* 
  
			A 4-element array containing a button's color while it's pressed.


	  - **onClickFunction**:  *function* 
  
			The function that should be called when a button is clicked.


	  - **type**:  *string* 
  
			A string containing the UI Element's type, can be "button" or "char".


  	- **char**: *string* 
  
		  A 1-character string that contains the UI Text's character.
  
  	- **Create**(Type = "button", Letter = 'A'): *function* 
  
		  A function that creates a UI Element.
		  
		- Parameters: 
  
		  - **Type**: A string that determines UI Element's type.
		  - **Letter**: A string character that contains the UI character.

  	- **DrawUI**(mouseX = 0, mouseY = 0, TextureCoordX1 = 0, TextureCoordX2 = 0, TextureCoordY1 = 0, TextureCoordY2 = 0, WidthToHeightRatio = 1): *function* 
  
		  A function that draws UI elements. must be constantly called in game's draw function.
		  
		- Parameters: 
  
		  - **mouseX**: Pointer's X position.
		  - **mouseY**: Pointer's Y position.
		  - **TextureCoordX1 **: Button sprite's start X point in the spritesheet.
		  - **TextureCoordX2 **: Button sprite's end X point in the spritesheet.
		  - **TextureCoordY1 **: Button sprite's start Y point in the spritesheet.
		  - **TextureCoordY2 **: Button sprite's end Y point in the spritesheet.
		  - **WidthToHeightRatio**: Button sprite's width to height ratio.

  	- **setOnClick**(fun): *function* 
  
		  A function that sets the function that should be called whenever UI button is clicked.
		  
		- Parameters: 
  
		  - **fun**: The function that should be called when UI button is clicked.


# **Variables**:


  - **GameObjects**: *list*
		---  A list that contains all active GameObject instances in the game.

  - **UIs**: *list*
		---  A list that contains all active UI instances in the game.


# **Functions**:


  - **drawText**(text = "text", textPosition = [0,0,0], textSize = 1, textColor = [1,1,1,1]): *function*

		A function that directly draws a text on the screen, using a custom font.

	- Parameters:
		- **text**: A string that contains the text that should be shown on screen.
		- **textPosition**: A 3-element array that contains the text's position.
		- **textSize**: A float that sets text size.
		- **textColor**: A 4-element array containing text's color.

  - **drawChar**(char = "A", charPosition = [0,0,0], charSize = 1, charColor = [1,1,1,1]): *function*

		A function that directly draws a text on the screen, using a custom font.

	- Parameters:
		- **char**: A string that contains the character that should be shown on screen.
		- **charPosition**: A 3-element array that contains the char's position.
		- **charSize**: A float that sets charsize.
		- **charColor**: A 4-element array containing char color.




---
---
---
---
- **Notes**:
	-  Font included is Rick and Morty's Calligraphr-Regular font, I do NOT own it. If you wish to use this engine for non-personal use, make sure to contact font owner and ask for permission.
	- Included images and sounds are only for test purposes, no copyright infringement intended. do NOT use for non-personal purposes before contacting media owners and asking them for permission. Otherwise, it is your responsibility.
---
---
---
---

