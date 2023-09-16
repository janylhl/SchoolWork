package org.openjfx;

import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.control.Label;
import javafx.scene.layout.VBox;

public class Top {
    Label welcomelabel;
    public VBox top() {
        VBox root = new VBox();
        root.setAlignment(Pos.CENTER);
        root.setPadding(new Insets(10));
        root.setSpacing(10);

        welcomelabel = new Label("Bienvenu sur notre outil de décision vous permettant de choisir différentes fusées," +
                "catalogues mais également sur mesure, afin d'obtimiser votre futur mission.");

        root.getChildren().addAll(welcomelabel);
        return root;
    }
}
