vcl 4.0;

backend default {
  .host = "wordpress";
  .port = "80";
}

sub vcl_recv{

  if(req.url ~ "wp-(login|admin)"){
    return(pass);
  }
}
