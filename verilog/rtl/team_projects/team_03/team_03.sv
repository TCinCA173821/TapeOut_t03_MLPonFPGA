`default_nettype none
// Empty top module

module top (
  // I/O ports
  input  logic clk, n_rst,
  input  logic [7:0] mosi,
  input  logic cs, sclk, start,
  output logic Done, nxtpckt_to_pi,
  output logic [3:0] result
);

  logic SPI_dv, MAC_s, MAC_l, HLBren, HLBincr, HLBwen, OLBincr, OLBwen, nxtpckt, ARG_s;
  logic [31:0] SPI_reg;
  logic [3:0] HLBrdata;
  logic [31:0] MAC_in;
  logic [63:0] MAC_out;
  logic [15:0] MAC_outrelu;
  logic [15:0] OLBrdata;
  logic [3:0] OLBrptr;
  

  controllertop main1(.*);
  SPI_mod spisys1(.*);
  genvar i;
    generate
        for (i = 0; i < 4; i = i + 1) begin : gen_mac
          MAC MAC_inst (.*,.MAC_in(MAC_in[8*i +:8]),.MAC_out(MAC_out[16*i +:16]),.MAC_outrelu(MAC_outrelu[4*i +:4]));
        end
    endgenerate
  hidden_layer_buffer hlb1 (.*, .nrst(n_rst),.wen(HLBwen),.ren(HLBren),.incr(HLBincr),.in(MAC_outrelu),.out(HLBrdata));
  output_layer_buffer olb1 (.*,.nrst(n_rst),.wen(OLBwen),.r_inc(OLBincr),.in(MAC_out),.out_data(OLBrdata),.rptr(OLBrptr));
  argmax argmax1 (.*,.nrst(n_rst),.start(ARG_s),.in(OLBrdata),.in_ptr(OLBrptr),.out(result));
  
endmodule