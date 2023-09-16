package org.openjfx;
import com.company.*;
import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.layout.VBox;

import java.util.ArrayList;

public class Right {
    public VBox right() {
        VBox root = new VBox();
        root.setPadding(new Insets(10));
        root.setSpacing(1);

        ArrayList<Item> items = new ArrayList();
        items = Simulation.loadItems(Left.monFichier);
        int n = items.size();
        for (int i=0; i<n; i++){
            Label currentlabel = new Label("Item"+i+":\n Nom: " + items.get(i).getName()+ "\n Poids :" + items.get(i).getWeight()+ "kg \n Prix :" + items.get(i).getCost()+ " euros \n Vies :" + items.get(i).getLife()+"\n");
            root.getChildren().addAll(currentlabel);

        }

        return root;
    }
}
