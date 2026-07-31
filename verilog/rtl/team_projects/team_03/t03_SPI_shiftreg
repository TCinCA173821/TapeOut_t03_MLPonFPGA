module SPI_shiftreg (
    input logic sclk,
    input logic cs,
    input logic n_rst,
    input logic [7:0] mosi,
    output logic [31:0] SPI_reg
);

    logic [31:0] intreg, regnxt;

    always_ff @ (posedge sclk, negedge n_rst) begin
        if(!n_rst) intreg <= 32'b0;
        else intreg <= regnxt;
    end

    always_comb begin
        regnxt = cs ? {intreg[23:0],mosi} : intreg;
    end
    assign SPI_reg = intreg;
endmodule
