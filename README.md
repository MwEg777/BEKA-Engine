
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

● **SpriteRenderer**: A class that enables game objects to have a sprite, and renders it.

  - Features:
  
	  - **flipX** :  *bool* 
  
			Bool that flips sprite in X axis when enabled.
  
	  - **flipY** :  *bool*
  
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
