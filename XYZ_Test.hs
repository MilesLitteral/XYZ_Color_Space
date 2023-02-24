{-# LANGUAGE FlexibleContexts #-}
{-# LANGUAGE ScopedTypeVariables #-}
{-# LANGUAGE RecordWildCards  #-}
{-# LANGUAGE TypeApplications #-}

module Main where
import           Control.Arrow
import           Control.Concurrent
import           Control.Monad.Random
import           Control.Monad.Reader
import           Data.Colour.RGBSpace
import           Data.Colour.RGBSpace.HSV
import           Data.Foldable            (for_)
import           Data.List                (nub)
import           Data.Semigroup           ((<>))
import           Data.Time.Clock.POSIX
import           Graphics.Rendering.Cairo
import           Linear.V2
import           Linear.Vector
import qualified Numeric.Noise.Perlin     as P
import           Text.Printf
import           Linear.V3

findX :: (Integral b, Fractional (b -> a), Fractional (a -> b -> a), Num a, Ord (b -> a)) => (b -> a) -> a -> b -> a
findX x = 
    if (x > 0.008856) 
    then return pow(x, 1 / 3.0) 
    else return (7.787 * x) + (16.0 / 116.0)

findY :: (Integral b, Fractional (b -> a), Fractional (a -> b -> a), Num a, Ord (b -> a)) => (b -> a) -> a -> b -> a
findY y = 
    if (y > 0.008856)
    then return pow(y, 1 / 3.0)
    else return (7.787 * y) + (16.0 / 116.0)

findZ :: (Integral b, Fractional (b -> a), Fractional (a -> b -> a), Num a, Ord (b -> a)) => (b -> a) -> a -> b -> a
findZ z = 
    if (z > 0.008856)
    then return pow(z, 1 / 3.0)
    else return (7.787 * z) + (16.0 / 116.0)

pow :: (Num a, Integral b) => a -> b -> a
pow value expo = value ^ expo

--dotprod :: (Num r, Num g, Num b) => r -> g -> b -> Integer
dotprod r g b = (r + g + b) - 128

--xyzColor :: (Num x, Num y, Num z) => x -> y -> z -> V3
xyzColor cx cy cz = do 
    let l = 116 * findY (cx / 95.047) - 16
    let a = 500 * findX (cx / 95.047) - findY (cy / 100.0)
    let b = 200 * findY (cy / 100.0) -  findZ (cz / 108.883)
    return $ V3 (l, a, b)

getSize :: Num a => Generate (a, a)
getSize = do
  (w, h) <- asks (worldWidth &&& worldHeight)
  pure (fromIntegral w, fromIntegral h)

fillScreen :: (Double -> Render a) -> Double -> Generate ()
fillScreen color opacity = do
  (w, h) <- getSize @Double
  cairo $ do
    rectangle 0 0 w h
    color opacity *> fill

teaGreen :: Double -> Render ()
teaGreen = hsva 81 0.25 0.94

vividTangerine :: Double -> Render ()
vividTangerine = hsva 11 0.40 0.92

englishVermillion :: Double -> Render ()
englishVermillion = hsva 355 0.68 0.84

darkGunmetal :: Double -> Render ()
darkGunmetal = hsva 170 0.30 0.16

renderSketch :: Generate ()
renderSketch = do
  fillScreen eggshell 1

  cairo $ setLineWidth 0.15

  quads <- genQuadGrid
  noisyQuads <- traverse quadAddNoise quads

  for_ noisyQuads $ \quad -> do
    strokeOrFill <- weighted [(fill, 0.4), (stroke, 0.6)]
    color <- uniform
       [ teaGreen
       , vividTangerine
       , englishVermillion
       , darkGunmetal
       ]
    cairo $ do
      renderQuad quad
      color 1 *> strokeOrFill

main :: IO()
main = do
    let xyz = xyzColor $ V3 (204 105 255)
    let normalVal = dotprod $ xyz ^. _1 xyz ^. _2 xyz ^. _3
    print $ show xyz
    print normalVal

