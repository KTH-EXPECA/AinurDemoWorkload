instructions.pdf: instructions.md
	pandoc \
		--variable fontsize=11pt \
		--number-sections \
		-f markdown  $< \
		--pdf-engine=xelatex \
		-o $@