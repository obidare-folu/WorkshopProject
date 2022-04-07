{% extends "base.html" %}

{% block title %}My Budget{% endblock %}

{% block content %}
<table>
    <tr>
        <th>Category</th>
        <th>Percentage</th>
        <th>Amount</th>
    </tr>
    <?php
    $conn = mysqli_connect("localhost", "root", "", "folusbudget")
    if ($conn-> connect_error) {
        die("Connection failed:". $conn-> connect_error);
    }

    $sql = "SELECT category, percentage, amount from Budget";
    $result = $conn-> query($sql)

    if ($result-> num_rows > 0) {
        while ($row = $result-> fetch_assoc()) {
            echo "<tr><td>". $row["category"] ."</td><td>". $row["percentage"] ."</td><td>". $row["amount"] ."</td></tr>";

        }
    echo "</table>"
    }
    else {
        echo "You have no Budgets"
    }
    $conn-> close();
    ?>
</table>
{% endblock %}
