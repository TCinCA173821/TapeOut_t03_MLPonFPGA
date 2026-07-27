
# Designs for bus wrap generation and initialization
PATTERNS = gpio_control la_control $(addprefix team_projects/, $(basename $(notdir $(shell find ./team_projects -mindepth 1 -maxdepth 1 -type d))))

#Bus Wrap Initialize
.PHONY: initialize
initialize:  ${PATTERNS}
	for i in ${PATTERNS}; do \
		( cd $$i &&\
			make generate_wb_yaml \
		) ; \
	done

#Bus Wrap Generate
generate:  ${PATTERNS}
	@for i in ${PATTERNS}; do \
		( cd $$i &&\
		 	make generate_wb_wrapper \
		) ; \
	done