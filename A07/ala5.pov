#include "ala.pov"

#declare pentagon_radius = 10.5;

object {
  mol_0
  translate mol_0_center
  translate <0, pentagon_radius, 0>
}

object {
  mol_0
  translate mol_0_center
  translate <0.951057*pentagon_radius, 0.309017*pentagon_radius, 0>
}

object {
  mol_0
  translate mol_0_center
  translate <0.587785*pentagon_radius, -0.809017*pentagon_radius, 0>
}

object {
  mol_0
  translate mol_0_center
  translate <-0.587785*pentagon_radius, -0.809017*pentagon_radius, 0>
}

object {
  mol_0
  translate mol_0_center
  translate <-0.951057*pentagon_radius, 0.309017*pentagon_radius, 0>
}
