#version 330

out float value_1;
out float value_2;

void main() {
    value_1 = gl_VertexID;
    value_2 = gl_VertexID * 2;
}
