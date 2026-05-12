
module tt_um_znielsen123 (
    input  wire [7:0] ui_in,
    output wire [7:0] uo_out,
    input  wire [7:0] uio_in,
    output wire [7:0] uio_out,
    output wire [7:0] uio_oe,
    input  wire       ena,
    input  wire       clk,
    input  wire       rst_n
);

    // For now, simple example behavior matching your current test:
    // ui_in = first 8-bit number
    // uio_in = second 8-bit number
    // uo_out = sum
    assign uo_out = ui_in + uio_in;

    // Not using bidirectional outputs
    assign uio_out = 8'b0;
    assign uio_oe  = 8'b0;

    // Avoid unused warnings
    wire _unused = &{ena, clk, rst_n, 1'b0};

endmodule
