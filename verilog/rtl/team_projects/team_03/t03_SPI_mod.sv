module SPI_mod (
    input logic clk,
    input logic n_rst,
    input logic nxtpckt,
    input logic cs,
    input logic sclk,
    input logic [7:0] mosi,
    output logic nxtpckt_to_pi,
    output logic SPI_dv,
    output logic [31:0] SPI_reg
);
    logic sync_cs;
    SPI_shiftreg spireg(.*);
    dualffsync sync_cs_f_fsm(.clk(clk),.n_rst(n_rst),.async_in(cs),.sync_out(sync_cs));
    SPI_FSM controler(.*);
endmodule
