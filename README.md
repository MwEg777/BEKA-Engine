
# BEKA Engine
A Python-based 2D Game engine, inspired by Unity3D

Example project included.

# Usage
1/Open GameLauncher.Py

2/Modify "Keeper" to your Game project file name. Eg: if your game file is called MyGame.Py, replace Keeper with MyGame

3/Run GameLauncher.Py


**-Note: PyGame is required to load images. To install it, open a cmd window and type: pip install pygame**


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

● **GameImages**: A class that enables you to use image files in the game, mostly to use with Sprites.

  - Properties and Methods:
	  -	
  
	  - **currentImage**:  *int* 
  
			A Read-Only integer value that determines which image is currently in use. 
			
	  - **imageCount**:  *int* 
  
			An integer value that determines the amount of image files to load by the game engine.

  	- **addImage**(imageName): *function* 
  
		  A function that adds an image file to the images loaded by the game engine.
  
		- Parameters: 
  
		  - **imageName**: A string that provides the name of the image file followed by the file extension. Eg: Beka.png, Game.jpg, ...

  	- **curImage**(CurrentImage = 1): *function* 
  
		  A function that sets the current image file in use.
  
		- Parameters: 
  
		  - **CurrentImage**: An integer value that is used to select an image to use.

  	- **getImageCount**(): *function* 
  
		  A function that returns the amount of images that are loaded by the game engine.
  
		- Parameters: 
  
		  - **CurrentImage**: An integer value that is used to select an image to use.
