#include <cmath>
#include <iostream>

#include "CLUE/ConvolutionalKernels.h"

#define DOCTEST_CONFIG_IMPLEMENT_WITH_MAIN
#include "doctest.h"

namespace ALPAKA_ACCELERATOR_NAMESPACE {

TEST_CASE("Test the flat kernel") {
  CHECK(FlatKernel(.5)(0., 0, 0) == 1.);
  CHECK(FlatKernel(.5)(1.5, 0, 0) == 1.);
  CHECK(FlatKernel(.5)(0., 1, 0) == .5);
  CHECK(FlatKernel(.5)(0., 0, 1) == .5);
  CHECK(FlatKernel(.5)(1.5, 0, 1) == .5);
}

TEST_CASE("Test the gaussian kernel") {
  CHECK(GaussianKernel(1.5, 1., 1.)(0., 0, 0) == 1.);
  CHECK(GaussianKernel(1.5, 1., 1.)(2., 0, 0) == 1.);
  CHECK(doctest::Approx(GaussianKernel(1.5, 1., 1.)(0., 1, 0)).epsilon(0.000001) ==
        std::exp(-(1.5 * 1.5) / 2));
  CHECK(doctest::Approx(GaussianKernel(1.5, 1., 1.)(0., 0, 1)).epsilon(0.000001) ==
        std::exp(-(1.5 * 1.5) / 2));
  CHECK(doctest::Approx(GaussianKernel(1.5, 1., 1.)(2., 0, 1)).epsilon(0.000001) ==
        std::exp(-(0.5 * 0.5) / 2));
}

TEST_CASE("Test the exponential kernel") {
  CHECK(ExponentialKernel(.5, 1.)(0., 0, 0) == 1.);
  CHECK(ExponentialKernel(.5, 1.)(2., 0, 0) == 1.);
  CHECK(ExponentialKernel(.5, 1.)(0., 1, 0) == 1.);
  CHECK(ExponentialKernel(.5, 1.)(0., 0, 1) == 1.);
  CHECK(doctest::Approx(ExponentialKernel(.5, 1.)(2., 0, 1)).epsilon(0.000001) == std::exp(-1.));
}
};
