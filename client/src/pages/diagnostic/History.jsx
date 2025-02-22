import React, { Component } from 'react';
import { NavigationBarDiagnostic, Footer } from '../../components';

function History() {
    return (
        <>
            <div>
                <NavigationBarDiagnostic></NavigationBarDiagnostic>
                <div class="callout-info">Historial de Diagnostico</div>
                <Footer></Footer>
            </div>

        </>
    )

}

export default History;