<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                              xmlns:csep="http://www.scec.org/xml-ns/csep/randomnumbers/0.1">

    <xsl:output method="text" encoding="UTF-8" indent="no"/>

    <xsl:template match="/">
        <xsl:apply-templates select="csep:CSEPRandomNumbers/csep:seed"/>
    </xsl:template>
    
    <xsl:template match="csep:CSEPRandomNumbers/csep:seed">
        <xsl:value-of select="."/>
<!-- leave <xsl:text> tags exactly in place, otherwise formatting will be messed up -->
<xsl:text>
</xsl:text>
    </xsl:template>
    
</xsl:stylesheet>