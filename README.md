This is an Experiment to create an algorithm that can create normal maps from a given albedo image. RGB is converted into X(R) Y(G) Z(B) data which can then be fed as a normal map. The appeal of the algorithm is to get a true representation of the albedo in normal space
striving for a photo realistic effect. There is one module supplied (XYZ_Test) in Python or Haskell. If you wish to import the library you can do the following:

==Python==
Download the XYZ_Test.py and import what you neeed from it into your project directly ie: `from ./xyz_test import x`

==Haskell== 
You can download the associated stack.yaml it downloads extra modules like JuicyPixels to condone it's function.
You can then expand upon the XYZ_Test.hs or import it's functions into your desired Haskell application.
